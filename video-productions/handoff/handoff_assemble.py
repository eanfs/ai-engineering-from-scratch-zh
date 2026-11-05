#!/usr/bin/env python3
"""Assemble one MiniMax Design episode into the delivery film.

Takes the clips downloaded by handoff_maxdesign.py fetch
(<job>/outputs/maxdesign/p01a.mp4, p02a.mp4, p02b.mp4, ...) plus the local
narration master and alignment, and produces a film that matches the local
hand-drawn episodes: 1920x1080, 30 fps, H.264 + AAC, burned-in captions,
0.65 s end hold and 0.55 s fade.

Usage (run with the skill virtualenv, it needs numpy and Pillow):

  VENV=~/.cache/sweety-handdraw-video/venv/bin/python
  $VENV video-productions/handoff/handoff_assemble.py 07-07-gpt-causal-lm
  $VENV video-productions/handoff/handoff_assemble.py 07-07-gpt-causal-lm --preview

--preview ignores the clips and animates the local hand-drawn page images
instead, so the whole chain can be rehearsed at zero cost. It writes
outputs/maxdesign/preview.mp4 and never touches film.mp4.

Outputs: <job>/outputs/maxdesign/{film.mp4,verification.json,verification.txt}
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

SKILL = Path.home() / ".hub/skills/handdrawn-explainer-video/scripts"
if not SKILL.is_dir():
    sys.exit(f"hand-drawn skill not found at {SKILL}")
sys.path.insert(0, str(SKILL))
import caption_assets  # noqa: E402

XFADE = 0.4


def run(command, **kwargs):
    result = subprocess.run(command, capture_output=True, text=True, **kwargs)
    if result.returncode:
        sys.exit(f"command failed: {' '.join(map(str, command))}\n{result.stderr[-3000:]}")
    return result


def probe(path):
    out = run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
               "-of", "json", str(path)]).stdout
    return json.loads(out)


def duration(path):
    return float(probe(path)["format"]["duration"])


def load(episode):
    hand = json.loads((Path(__file__).resolve().parent / f"{episode}.json").read_text())
    job = Path(__file__).resolve().parents[2] / hand["source_job"]
    return hand, job


def page_boundaries(job, hand):
    """Page windows in seconds; page 1 starts at 0 to cover the lead-in."""
    alignment = json.loads((job / "inputs/narration/alignment.json").read_text())
    total = duration(job / "inputs/narration/master.wav")
    first = {}
    order = []
    for beat in alignment["beats"]:
        page = beat["id"].split("-")[0]
        if page not in first:
            first[page] = beat["start"]
            order.append(page)
    names = [page["page"] for page in hand["pages"]]
    if order != names:
        sys.exit(f"alignment pages {order} do not match handoff pages {names}")
    bounds = [0.0] + [first[name] for name in order[1:]] + [total]
    return alignment, bounds, total


def frame_edges(boundaries, fps):
    """Cumulative frame boundaries, so page segments sum to the exact total."""
    edges = [round(value * fps) for value in boundaries]
    return [edges[i + 1] - edges[i] for i in range(len(edges) - 1)]


def paper_input(paper, canvas, seconds):
    return ["-f", "lavfi", "-i",
            f"color=c={paper}:s={canvas[0]}x{canvas[1]}:r=30:d={seconds:.3f}"]


def still_segment(source, seconds, out, canvas, inset, paper, frames=None):
    """Preview page: the still, slowly zooming, on the same paper inset the
    local renderer uses, so captions keep the margin below."""
    x, y, box_w, box_h = inset
    frames = frames or round(seconds * 30)
    zoom = (f"zoompan=z='min(zoom+0.00035,1.06)':x='iw/2-(iw/zoom/2)':"
            f"y='ih/2-(ih/zoom/2)':d={max(frames, 2)}:s={box_w}x{box_h}:fps=30")
    run(["ffmpeg", "-y", "-loop", "1", "-i", str(source),
         *paper_input(paper, canvas, seconds),
         "-filter_complex",
         f"[0:v]scale={box_w}:{box_h}:force_original_aspect_ratio=increase,"
         f"crop={box_w}:{box_h},{zoom},setsar=1[img];"
         f"[1:v][img]overlay={x}:{y}:shortest=1[v]",
         "-map", "[v]", "-frames:v", str(frames), "-an",
         "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", str(out)])


def clip_segment(sources, seconds, out, canvas, work, inset, paper, frames=None):
    """Join a page's clips (cross-fade between parts) and retime to its window."""
    x, y, box_w, box_h = inset
    frames = frames or round(seconds * 30)
    durations = [duration(path) for path in sources]
    if len(sources) == 1:
        joined = work / "joined.mp4"
        run(["ffmpeg", "-y", "-i", str(sources[0]), "-an", "-c", "copy", str(joined)])
        joined_seconds = durations[0]
    else:
        joined = work / "joined.mp4"
        command = ["ffmpeg", "-y"]
        for path in sources:
            command += ["-i", str(path)]
        chains = []
        for i in range(len(sources)):
            chains.append(f"[{i}:v]fps=30,scale={box_w}:{box_h}:"
                          f"force_original_aspect_ratio=increase,crop={box_w}:{box_h},"
                          f"setsar=1,settb=AVTB,setpts=PTS-STARTPTS[v{i}]")
        offset = 0.0
        label = "[v0]"
        joined_seconds = durations[0]
        for i in range(1, len(sources)):
            offset += durations[i - 1] - XFADE
            joined_seconds += durations[i] - XFADE
            chains.append(f"{label}[v{i}]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}[x{i}]")
            label = f"[x{i}]"
        command += ["-filter_complex", ";".join(chains), "-map", label,
                    "-an", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", str(joined)]
        run(command)
    # Retime the joined clip onto the page window without changing its look.
    factor = seconds / joined_seconds
    if not 0.5 <= factor <= 1.35:
        sys.exit(f"{out.name}: page needs {seconds:.2f}s but the clips give "
                 f"{joined_seconds:.2f}s ({factor:.2f}x); regenerate with clip_plan")
    run(["ffmpeg", "-y", "-i", str(joined),
         *paper_input(paper, canvas, seconds),
         "-filter_complex",
         f"[0:v]setpts=PTS*{factor:.6f},fps=30,setsar=1,"
         f"scale={box_w}:{box_h}:force_original_aspect_ratio=increase,"
         f"crop={box_w}:{box_h}[img];"
         f"[1:v][img]overlay={x}:{y}:shortest=1[v]",
         "-map", "[v]", "-frames:v", str(frames), "-an",
         "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", str(out)])


def cover_segment(source, seconds, out, canvas, frames=None):
    """Full-frame cover, held for the declared cover_seconds."""
    frames = frames or round(seconds * 30)
    run(["ffmpeg", "-y", "-loop", "1", "-i", str(source), "-t", f"{seconds:.3f}",
         "-vf", f"scale={canvas[0]}:{canvas[1]}:force_original_aspect_ratio=increase,"
                f"crop={canvas[0]}:{canvas[1]},setsar=1",
         "-fps_mode", "cfr", "-r", "30", "-frames:v", str(frames), "-an",
         "-c:v", "libx264", "-crf", "16",
         "-pix_fmt", "yuv420p", str(out)])


def hold_last(segment, seconds, out, canvas, frames=None):
    """Freeze the last frame of the film for the end hold."""
    last = out.with_suffix(".last.png")
    run(["ffmpeg", "-y", "-sseof", "-0.5", "-i", str(segment),
         "-frames:v", "1", "-update", "1", str(last)])
    frames = frames or round(seconds * 30)
    run(["ffmpeg", "-y", "-loop", "1", "-i", str(last), "-t", f"{seconds:.3f}",
         "-vf", f"scale={canvas[0]}:{canvas[1]},setsar=1",
         "-fps_mode", "cfr", "-r", "30", "-frames:v", str(frames), "-an",
         "-c:v", "libx264", "-crf", "16",
         "-pix_fmt", "yuv420p", str(out)])


def page_inset(job, canvas):
    """Where the local renderer places a page illustration; captions live below it."""
    width, height = canvas
    for page in job.get("pages", []):
        for group in page.get("visual_groups", []):
            for action in group.get("actions", []):
                if action.get("type") == "illustration":
                    return (int(action["x"]), int(action["y"]),
                            int(action["width"]), int(action["height"]))
    return (width // 6, height // 9, width * 2 // 3, height * 2 // 3)


def caption_canvas(job, alignment, canvas, directory, offset=0.0):
    """Full-canvas RGBA frames, one per caption cue, plus their time window."""
    width, height = canvas
    options = dict(job.get("captions") or {})
    options.setdefault("font", job.get("font") or {})
    directory.mkdir(parents=True, exist_ok=True)
    cues = []
    for beat in alignment["beats"]:
        base = float(beat["start"])
        for index, cue in enumerate(beat["caption_cues"]):
            name = f"{beat['id']}-{index}"
            caption_assets.build_caption(directory, name, cue["text"],
                                         options, width, height)
            strip = Path(directory) / f"{name}.png"
            canvas_image = np.zeros((height, width, 4), dtype=np.uint8)
            with_strip = Image.open(strip).convert("RGBA")
            x = (width - with_strip.width) // 2
            y = height - with_strip.height - int(options.get("bottom_margin", 0))
            layer = np.array(with_strip)
            target = canvas_image[y:y + layer.shape[0], x:x + layer.shape[1]]
            alpha = layer[..., 3:4].astype(np.float32) / 255.0
            target[..., :3] = (layer[..., :3] * alpha +
                               target[..., :3] * (1 - alpha)).astype(np.uint8)
            target[..., 3] = np.maximum(target[..., 3], layer[..., 3])
            full = directory / f"{name}-full.png"
            Image.fromarray(canvas_image).save(full)
            cues.append({"window": (offset + base + float(cue["start"]),
                                    offset + base + float(cue["end"])),
                         "path": full, "text": cue["text"],
                         "width": with_strip.width, "height": with_strip.height,
                         "y": y})
    if not cues:
        sys.exit("alignment has no caption cues")
    return cues


def caption_frames(cues, total, fps, width, height):
    """Yield one RGBA frame per output frame, with the active cue burned in."""
    frames = round(total * fps)
    starts = [round(window["window"][0] * fps) for window in cues]
    ends = [round(window["window"][1] * fps) for window in cues]
    blank = np.zeros((height, width, 4), dtype=np.uint8)
    cached = {}
    index = 0
    for frame in range(frames):
        while index < len(cues) and frame >= ends[index]:
            index += 1
        if index < len(cues) and starts[index] <= frame < ends[index]:
            if index not in cached:
                cached[index] = np.array(
                    Image.open(cues[index]["path"]).convert("RGBA"))
            yield cached[index].tobytes()
        else:
            yield blank.tobytes()


def assemble(hand, job, preview):
    canvas = (hand["canvas"]["width"], hand["canvas"]["height"])
    fps = hand["canvas"]["fps"]
    alignment, bounds, speech_end = page_boundaries(job, hand)
    job_data = json.loads((job / "job.json").read_text())
    inset = page_inset(job_data, canvas)
    paper = job_data.get("paper", "#FFFDF7")
    cover_seconds = float(job_data.get("cover", {}).get("seconds", 0))
    hold = float(job_data.get("audio", {}).get("end_hold_seconds", 0))
    total = cover_seconds + speech_end + hold

    out_dir = job / "outputs/maxdesign"
    work = job / "work/maxdesign"
    out_dir.mkdir(parents=True, exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)

    edges = [cover_seconds] + [cover_seconds + value for value in bounds[1:]]
    plan = [(edges[i], edges[i + 1] - edges[i]) for i in range(len(edges) - 1)]
    counts = frame_edges([0.0] + edges + [total], fps)
    cover_frames, page_frames, tail_frames = counts[0], counts[1:-1], counts[-1]
    print(f"  cover {cover_seconds:5.2f}s  {job_data['cover']['source']}")
    print(f"  tail  {hold:5.2f}s  total {total:.3f}s")

    segments = []
    cover_target = work / "seg-cover.mp4"
    if cover_seconds > 0:
        cover_segment(job / job_data["cover"]["source"], cover_seconds,
                      cover_target, canvas, cover_frames)
        segments.append(cover_target)
    for page, (_, seconds), frames in zip(hand["pages"], plan, page_frames):
        target = work / f"seg-{page['page']}.mp4"
        print(f"  {page['page']}  {seconds:6.2f}s  {page['title']}")
        if preview:
            still_segment(job / f"inputs/{page['page']}.png", seconds, target,
                          canvas, inset, paper, frames)
        else:
            names = [f"{page['page']}{chr(ord('a') + i)}"
                     for i in range(len(page["clip_plan"]))]
            sources = [out_dir / f"{name}.mp4" for name in names]
            missing = [str(path) for path in sources if not path.is_file()]
            if missing:
                sys.exit(f"missing clips: {', '.join(missing)}; run fetch first "
                         f"(or use --preview)")
            clip_segment(sources, seconds, target, canvas, work, inset, paper, frames)
        segments.append(target)

    if hold > 0:
        tail_target = work / "seg-tail.mp4"
        tail_source = segments[-1]
        hold_last(tail_source, hold, tail_target, canvas, tail_frames)
        segments.append(tail_target)

    listing = work / "segments.txt"
    listing.write_text("".join(f"file '{path}'\n" for path in segments))
    base = work / "base.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
         "-fps_mode", "cfr", "-r", "30", "-an", "-c:v", "libx264", "-crf", "16",
         "-pix_fmt", "yuv420p", str(base)])

    cues = caption_canvas(job_data, alignment, canvas, work / "captions",
                          offset=cover_seconds)
    name = "preview.mp4" if preview else "film.mp4"
    film = out_dir / name
    fade = float(hand.get("fade_seconds", 0.55))
    audio_filter = (f"adelay={round(cover_seconds * 1000)}:all=1,"
                    f"apad=pad_dur={hold:.3f},loudnorm=I=-17:TP=-2:LRA=7")
    command = ["ffmpeg", "-y", "-i", str(base),
               "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{canvas[0]}x{canvas[1]}",
               "-r", str(fps), "-i", "-",
               "-i", str(job / "inputs/narration/master.wav"),
               "-filter_complex",
               f"[0:v][1:v]overlay=0:0:format=auto[c];"
               f"[c]fade=t=out:st={max(total - fade, 0):.3f}:d={fade:.3f}[v];"
               f"[2:a]{audio_filter}[a]",
               "-map", "[v]", "-map", "[a]",
               "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
               "-t", f"{total:.3f}", str(film)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE,
                               stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    assert process.stdin is not None and process.stderr is not None
    try:
        for payload in caption_frames(cues, total, fps, canvas[0], canvas[1]):
            process.stdin.write(payload)
    finally:
        process.stdin.close()
        error = process.stderr.read().decode()
        if process.wait():
            sys.exit(f"final encode failed:\n{error[-3000:]}")
    print(f"  wrote {film}  {film.stat().st_size} B")
    return film, total, fps, canvas

def verify(film, total, fps, canvas):
    report = {"film": film.name, "checks": {}}
    meta = probe(film)
    video = next(s for s in meta["streams"] if s["codec_type"] == "video")
    audio = next(s for s in meta["streams"] if s["codec_type"] == "audio")
    report["checks"]["dimensions"] = {
        "ok": (video["width"], video["height"]) == canvas,
        "value": [video["width"], video["height"]]}
    report["checks"]["frame_rate"] = {
        "ok": video["avg_frame_rate"] == f"{fps}/1", "value": video["avg_frame_rate"]}
    report["checks"]["codecs"] = {
        "ok": (video["codec_name"], audio["codec_name"]) == ("h264", "aac"),
        "value": [video["codec_name"], audio["codec_name"]]}
    video_duration = float(video["duration"])
    audio_duration = float(audio["duration"])
    report["checks"]["duration"] = {
        "ok": abs(video_duration - total) < 0.08 and abs(audio_duration - total) < 0.08,
        "value": [round(video_duration, 3), round(total, 3)]}
    decode = subprocess.run(["ffmpeg", "-v", "error", "-i", str(film), "-f", "null", "-"],
                            capture_output=True, text=True)
    report["checks"]["decode"] = {
        "ok": decode.returncode == 0 and not decode.stderr.strip(),
        "value": decode.stderr.strip()[:400]}
    volume = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(film),
                             "-af", "loudnorm=I=-17:TP=-2:LRA=7:print_format=json",
                             "-f", "null", "-"], capture_output=True, text=True)
    match = re.search(r"\{\s*\"input_i\".*?\}", volume.stderr, re.S)
    loudness = json.loads(match.group(0)) if match else None
    report["checks"]["loudness"] = {
        "ok": bool(loudness) and abs(float(loudness["input_i"]) + 17) <= 1.5,
        "value": loudness and loudness["input_i"]}
    return report


def audio_correlation(film, master, cover_seconds=0.0):
    def pcm(path):
        return np.frombuffer(subprocess.check_output(
            ["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1",
             "-ar", "48000", "-f", "f32le", "-"]), dtype="<f4")
    encoded, source = pcm(film), pcm(master)
    encoded = encoded[int(round(cover_seconds * 48000)):]
    common = min(len(encoded), len(source))
    if common == 0:
        return {"ok": False, "value": None}
    correlation = float(np.corrcoef(source[:common], encoded[:common])[0, 1])
    return {"ok": correlation > 0.99, "value": round(correlation, 7),
            "length_delta_seconds": round(abs(len(encoded) - len(source)) / 48000, 3)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("episode")
    parser.add_argument("--preview", action="store_true",
                        help="animate the local page images instead of the app clips")
    arguments = parser.parse_args()
    hand, job = load(arguments.episode)
    film, total, fps, canvas = assemble(hand, job, arguments.preview)
    report = verify(film, total, fps, canvas)
    cover_seconds = float(json.loads((job / "job.json").read_text())
                          .get("cover", {}).get("seconds", 0))
    report["checks"]["audio_correlation"] = audio_correlation(
        film, job / "inputs/narration/master.wav", cover_seconds)
    report["preview"] = arguments.preview
    report["ok"] = all(check["ok"] for check in report["checks"].values())
    out_dir = job / "outputs/maxdesign"
    (out_dir / "verification.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1) + "\n")
    lines = [f"{'PASS' if report['ok'] else 'FAIL'}  {film}",
             f"duration {total:.3f}s  canvas {canvas[0]}x{canvas[1]}  {fps} fps"]
    for name, check in report["checks"].items():
        lines.append(f"  {'ok  ' if check['ok'] else 'FAIL'}  {name}: {check['value']}")
    (out_dir / "verification.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    sys.exit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
