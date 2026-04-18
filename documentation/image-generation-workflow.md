# Image Generation Workflow

> How event images for the mod are produced. Verified end-to-end on 2026-04-17 with the Layla "The Deed" (homesteading) image as proof-of-concept.

---

## Tooling

- **Codex CLI** (`codex-cli 0.121.0`), authenticated via ChatGPT login (not API key).
- Config at `~/.codex/config.toml` has `features.image_generation = true` -- this enables the native image tool.
- Verify before first run:
  ```bash
  codex --version
  codex login status   # should say "Logged in using ChatGPT"
  grep image_generation ~/.codex/config.toml
  ```

No OpenAI API key is required; Codex uses the same auth as the ChatGPT app.

---

## Directory conventions

**Source images (outside the mod repo):**
```
/home/aboelsoud/Pictures/common-people-mod-images/
├── Layla/
│   ├── layla.png                           (canonical portrait, face reference)
│   ├── cp_layla_<event>.dds.png            (600x400 event images, game-ready size)
│   └── cp_layla_<event>_1536.png           (1536x1024 archive, for re-renders)
├── <other_character>/
│   ├── <name>.png
│   └── ...
```

**In-mod images** (shipped with the mod, DDS format required by V3):
```
mod/gfx/event_pictures/
├── cp_layla_homesteading.dds
└── ...
```

The `.dds.png` suffix in the source folder is a typo-friendly placeholder -- the file is a PNG, but we name it for the final DDS it will become after conversion. Keeps the eventify pass's `picture = "cp_layla_homesteading"` references stable.

---

## Prompt template

Every image prompt follows the same five-section structure. The reliability of the result is directly a function of how tight this prompt is; lazy prompts get generic fantasy-art.

```
Generate ONE event image for a Victoria 3 mod about Egyptian peasants.
This is for the event "<Event title>" (<event_id>) -- <one-sentence context of what happens in this scene>.

Reference images attached:
- First image (<character>.png): canonical portrait of <character> -- <physical description: age, hair, clothing, palette>. Match face, hair, clothing, and palette exactly.
- Second image (<prior event>.dds.png): visual style to match -- painterly oil, 19th-century genre painting, warm earth tones (ochre, sienna, cream), Egyptian rural setting, cinematic composition, 600x400 landscape aspect, slight painted-canvas texture.

Scene to generate: <who is in frame, what they are doing, where, what time of day, what specific physical details matter -- the deed in hand, the red wax seal, the bey on horseback in the middle distance, etc>.

Mood: <one-sentence description of register -- "quiet gravity, not celebration", "tension before a rupture", etc>. Mahfouz register in painted form.

Resolution: 3:2 landscape aspect, 600x400 if supported.

Save the final PNG to: <absolute target path>.dds.png

Report the final saved file path in your reply.
```

### Prompt gotchas learned the hard way

- **"ONE image"** in capitals matters; Codex has generated multi-panel composites without it.
- **Describe face explicitly** in the Reference Images section. Codex's image tool sees attached images as stylistic prompts, *not* as identity locks -- the generated face will be in the character's spirit but will drift across runs. Explicit facial description ("oval face, heavy brows, small mole under left eye") closes some of the gap but not all of it. True face-lock needs a different tool (see [Scaling](#scaling)).
- **Name the specific physical objects** that must appear (paper, wax seal, horse, ox-cart, specific garment). Abstract mood words without object anchors give mood paintings without narrative.
- **Mahfouz register** as a prompt phrase nudges composition toward quiet human scale rather than epic heroic framing. Useful even if the model has never read Mahfouz.

---

## Command pattern

```bash
cat <<'PROMPT_EOF' | codex exec --full-auto \
  -i /home/aboelsoud/Pictures/common-people-mod-images/Layla/layla.png \
  -i /home/aboelsoud/Pictures/common-people-mod-images/Layla/cp_layla_serfdom.dds.png
<full prompt body per template above>
PROMPT_EOF
```

### Flag notes

- `-i <file>` attaches a reference image. Repeat for multiple references. Order matters only in that it matches the order you cite them in the prompt body ("first image", "second image").
- `--full-auto` runs in sandboxed workspace-write mode and skips confirmation prompts. Required for hands-off runs.
- **Prompt via stdin** -- passing the prompt as a positional argument after `-i` flags fails (the last `-i` greedily consumes the prompt). Piping via heredoc is the reliable pattern.

### Alternative: bypass the sandbox entirely

```bash
codex exec --dangerously-bypass-approvals-and-sandbox -i ... <<'EOF'
...
EOF
```

Use this only when the target directory is outside codex's default writable set (see [Sandbox gotcha](#sandbox-gotcha)). Treat it like `sudo` -- fine for this specific task, don't make it a habit.

---

## Sandbox gotcha

With `--full-auto`, codex writes are restricted to the project-root workspace. `/home/aboelsoud/Pictures/...` is *outside* that workspace and reads as read-only. The image generation itself works, but the final `cp` into the target directory fails with:

```
cp: cannot create regular file '.../cp_layla_<event>.dds.png': Read-only file system
```

Codex's workaround in that case: it scales and writes to `/tmp/common-people-mod-images/Layla/<name>.dds.png`. Two ways to finalize from there:

1. **Copy from outside the codex session.** After codex reports success and names its /tmp path, run:
   ```bash
   cp /tmp/common-people-mod-images/Layla/<name>.dds.png \
      /home/aboelsoud/Pictures/common-people-mod-images/Layla/
   cp /home/aboelsoud/.codex/generated_images/<session-id>/ig_<hash>.png \
      /home/aboelsoud/Pictures/common-people-mod-images/Layla/<name>_1536.png
   ```
   (The `_1536` archive is optional but cheap to keep -- it's the pre-downscale original, usable for re-renders at higher resolution later.)

2. **Run codex with full access.** Use `--dangerously-bypass-approvals-and-sandbox` as above. Codex writes directly to the target path. Single-command workflow, less copy-paste.

Recommendation: use option 1 for now. Option 2 becomes worth it when generating in bulk.

---

## Post-generation steps

After each image is in `/home/aboelsoud/Pictures/common-people-mod-images/<Character>/`:

1. **Eyeball it.** Is the character recognizable? Is the scene readable at 600x400? Is the mood right?
2. If unacceptable, **re-run** with a tightened prompt. Don't edit -- regenerate. It's cheap.
3. **Commit the PNG to the source folder** (already done by the copy step). That folder isn't in the mod repo and isn't checked into git; it's the asset library.
4. **Convert PNG -> DDS** for in-mod use. V3 requires `.dds` (BC3 / DXT5) for event pictures. One command covers every image in the asset library:
   ```bash
   ./script/convert-images-to-dds.sh
   ```
   The script prefers `nvcompress` (apt: `libnvtt-bin`) and falls back to ImageMagick's `magick`. Idempotent -- re-running only converts files whose PNG is newer than the existing DDS. See [event-workflow.md](event-workflow.md#step-4-convert-png--dds) for the script's behavior and env overrides.
5. **Drop the DDS into the mod:**
   ```
   mod/gfx/event_pictures/cp_<character>_<event>.dds
   ```
6. **Wire it in the event** (eventify pass):
   ```
   cp_<character>.<event> = {
       ...
       picture = {
           texture = "gfx/event_pictures/cp_<character>_<event>.dds"
       }
       ...
   }
   ```

Step 4 is wired: `script/convert-images-to-dds.sh` walks the Pictures folder and produces DDS siblings inside the mod. Install the converter once (`sudo apt install libnvtt-bin`) and the script runs hands-off thereafter.

---

## Proof-of-concept run (2026-04-17)

- Event: Layla homesteading (R2, "The Deed")
- Command: `codex exec --full-auto -i layla.png -i cp_layla_serfdom.dds.png` with stdin prompt
- Time: ~25 seconds end-to-end (prompt submission to saved PNG)
- Output: 1536x1024 original, downscaled via Codex's internal `ffmpeg` call to 600x400
- Cost: counted against ChatGPT subscription, not a separate API charge
- Result: acceptable composition and palette; face drifted ~20% from the portrait reference
- Archive: `~/.codex/generated_images/<session-id>/ig_<hash>.png` (the 1536x1024 original is kept by codex itself)

---

## Scaling

Generating ~150 event images (1 per reaction + 1 per distinctive pulse event) by this workflow is feasible -- call it ~1 hour of prompt-write + button-press time + copy-from-/tmp chores. Two improvements make that hour pleasant:

1. **Prompt generation from events.** Write a script that reads `reactions.md` and `pulse.md`, extracts `id`, `prose kernel`, and relevant state tags, and emits a ready-to-run codex command per event. Instead of hand-writing 150 prompts, hand-write the template once.
2. **Face-lock toolchain.** Codex's native image tool doesn't character-lock. For per-character consistency across 50 images of Layla, use an identity-reference tool:
   - **Midjourney with `--cref`** -- best out-of-box identity lock; paid subscription, web UI only.
   - **Ideogram Character Reference** -- similar, API available.
   - **ComfyUI + InstantID / IPAdapter FaceID** -- local, free, steep setup. SDXL-based; quality is good but not oil-painterly without careful prompting.
   - **Flux-Dev + PuLID** -- local, excellent identity; newer, less tooling around it.

Decision for now: keep using Codex for proof-of-concept per-character (one hero shot per character), then pick a face-lock tool before generating the full 150-image pool.

---

## Files this workflow produces (per event)

For event `cp_<character>_<event>`:

```
/home/aboelsoud/Pictures/common-people-mod-images/<Character>/
├── cp_<character>_<event>.dds.png          (600x400 PNG, ready for DDS conversion)
└── cp_<character>_<event>_1536.png         (1536x1024 archive, kept for re-renders)

mod/gfx/event_pictures/
└── cp_<character>_<event>.dds              (after PNG -> DDS conversion, shipped with the mod)
```

The mod itself ships only the `.dds`. The `.png` sources stay in the asset library for iteration and redo.
