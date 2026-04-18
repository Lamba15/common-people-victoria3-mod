#!/usr/bin/env bash
# Generate Layla event images via Codex CLI.
#
# Prerequisites (see documentation/image-generation-workflow.md):
#   - codex CLI installed and logged in via ChatGPT
#   - features.image_generation = true in ~/.codex/config.toml
#   - reference portrait and a canonical style image under
#     /home/aboelsoud/Pictures/common-people-mod-images/Layla/
#
# Usage:
#   script/gen-layla-event-images.sh             # generate all
#   script/gen-layla-event-images.sh cp_layla_no_wind cp_layla_mothers_hand
#     (pass specific names to regenerate a subset)
#
# After this runs, convert PNG -> DDS with:
#   script/convert-images-to-dds.sh

set -uo pipefail

ASSETS=/home/aboelsoud/Pictures/common-people-mod-images/Layla
LOGDIR=/tmp/codex-image-runs
mkdir -p "$LOGDIR"

REF_FACE="$ASSETS/layla.png"
REF_STYLE="$ASSETS/cp_layla_homesteading.dds.png"

run_one() {
  local name="$1"
  local title="$2"
  local context="$3"
  local scene="$4"
  local mood="$5"

  # Subset filter: if positional args were passed, skip anything not listed.
  if [ $# -lt 6 ]; then :; fi  # placeholder, per-call arity fixed at 5
  if [ ${#SELECTED[@]} -gt 0 ]; then
    local found=0
    for sel in "${SELECTED[@]}"; do
      if [ "$sel" = "$name" ]; then found=1; break; fi
    done
    [ $found -eq 0 ] && return 0
  fi

  local target="$ASSETS/${name}.dds.png"
  local logfile="$LOGDIR/${name}.log"

  echo "[$(date +%H:%M:%S)] === $name === starting"

  cat <<PROMPT_EOF | codex exec --dangerously-bypass-approvals-and-sandbox \
      -i "$REF_FACE" \
      -i "$REF_STYLE" >"$logfile" 2>&1
Generate ONE event image for a Victoria 3 mod about Egyptian peasants.
This is for the event "$title" ($name) -- $context.

Reference images attached:
- First image (layla.png): canonical portrait of Layla -- a Misri (Egyptian) peasant woman, 22 years old in 1836, oval face, dark hair, dark eyes, sun-warmed olive skin, traditional Lower Egyptian village wardrobe with a headscarf. Match face, hair, skin tone, clothing, and palette EXACTLY.
- Second image (cp_layla_homesteading.dds.png): visual style to match -- painterly oil, 19th-century genre painting, warm earth tones (ochre, sienna, cream), Egyptian rural setting, cinematic composition, 600x400 landscape aspect, slight painted-canvas texture, Mahfouz register.

Scene to generate: $scene

Mood: $mood. Mahfouz register in painted form.

Resolution: 3:2 landscape, 600x400 if supported.

Save the final PNG to: $target

Report the final saved file path in your reply.
PROMPT_EOF

  local rc=$?
  if [ $rc -eq 0 ] && [ -f "$target" ]; then
    echo "[$(date +%H:%M:%S)] === $name === OK -> $target"
  else
    echo "[$(date +%H:%M:%S)] === $name === FAILED (rc=$rc) -- see $logfile"
  fi
}

SELECTED=("$@")

###############################################################################
# 1. Intro -- "The Farmer's Daughter" (cp_layla.1)
###############################################################################
run_one "cp_layla_intro" \
  "The Farmer's Daughter" \
  "Layla rises before dawn in her Lower Egyptian village; she stands on the threshold of her mud-brick house and waits for the light" \
  "Layla stands on the threshold of a low mud-brick house at the edge of a Lower Egyptian fellah village. She wears a faded headscarf and a long dark dress. Behind her the Nile is a thin silver line in the middle distance. The sky is the color of the inside of a pomegranate -- pre-dawn, deep coral and indigo bands. A donkey is asleep in the lane. She is alone in frame, three-quarter view, looking out toward the river. No other people visible." \
  "quiet anticipation, the stillness before a long day, the beginning of a long story"

###############################################################################
# 2. Homesteading -- "The Deed" (cp_layla.2)
###############################################################################
run_one "cp_layla_homesteading_v2" \
  "The Deed" \
  "Egypt has just enacted homesteading; Layla receives a deed paper that says this patch of earth belongs to her" \
  "Layla stands in the middle of her own field, holding a folded deed paper sealed with a deep red wax seal. Her hands tremble visibly; she has never held a paper of her own before. Bright morning light. Behind her is a fellah field of green wheat or cotton, the village in the far distance. She looks at the paper, not at the camera. Three-quarter close-medium shot. Just her in frame." \
  "quiet gravity, not celebration; the weight of a thing she did not believe could happen"

###############################################################################
# 3. Serfdom restored -- "The Bey Returns" (cp_layla.3)
###############################################################################
run_one "cp_layla_serfdom_restored" \
  "The Bey Returns" \
  "A regime change has restored serfdom; the bey rides through the village again and Layla and Ahmed back against the wall of their house" \
  "Layla and her husband Ahmed (a wiry Misri man in his late twenties, simple grey gallabiya) press their backs against the mud-brick wall of their house in the village lane. In the middle distance, a mounted Ottoman-Egyptian bey on a dark horse rides through the lane; dust rising from hooves; a bey servant on foot beside him. Doors of nearby houses are shut. Late afternoon light, harsh and angled. Layla holds Ahmed's wrist. Her face is composed but her eyes are wide. Wide cinematic composition, the bey is small in frame but central, Layla and Ahmed in the foreground left." \
  "fear that has learned to be silent; the worst day, made of quiet"

###############################################################################
# 4. Ahmed conscripted -- "He Marches" (cp_layla.4)
###############################################################################
run_one "cp_layla_ahmed_conscripted" \
  "He Marches" \
  "War has started; Ahmed has been conscripted; he walks away in a column of village conscripts and Layla watches from the village edge" \
  "Layla stands at the edge of the village beside a low mud wall, watching a column of newly-conscripted Egyptian fellahin walking away down a dirt track raising dust. Ahmed is among them, recognizable by his grey gallabiya, looking back over his shoulder once. He carries a small bundle. The men are not in uniform yet -- they are villagers, marched off to be made soldiers. Other women and children stand farther down the wall, also watching. Mid-morning light. The column is in the middle distance moving away from the camera. Layla in the foreground left, her hand at her throat, no tears." \
  "the worst kind of leaving -- the kind that pretends, for the watcher's sake, that he will be back"

###############################################################################
# 5. Childbirth -- "The First Cry" (cp_layla.5)
###############################################################################
run_one "cp_layla_childbirth" \
  "The First Cry" \
  "Layla has survived childbirth; she holds her newborn for the first time in candlelight" \
  "Layla sits propped against pillows on a low bed in a small mud-brick room, holding a swaddled newborn in her arms. A single oil lamp on a wooden chest provides almost all the light. Her hair is undone and damp at the temples; she is exhausted, her face shining with sweat. The midwife (an older Misri woman) stands at the foot of the bed in shadow, drying her hands on a cloth. Ahmed kneels beside the bed, his hand on Layla's shoulder. Layla looks down at the baby, not at Ahmed. Warm amber lamplight, deep shadows in the corners of the room. Close-medium shot, Layla and the baby centered." \
  "exhausted reverence; the small private miracle of having survived, and a child having survived"

###############################################################################
# 13. A Day With No Wind -- cp_layla.13
###############################################################################
run_one "cp_layla_no_wind" \
  "A Day With No Wind" \
  "A windless, heavy morning in the Delta; Layla grinds dhurra in her mud-brick courtyard, praying quietly while she works" \
  "Layla crouches beside a low stone grinding-bowl in the packed-earth courtyard of her mud-brick house. Her hands rest on the upper grinding stone; a small pile of dhurra grain is beside her on a shallow tray. The air is heavy and still -- dust hangs motionless in the air, catching the light. A neighbour's lean cat walks along the top of the mud courtyard wall in the middle distance, stepping slowly. Two hens stand quietly, not scratching. The palm-frond roof of the house is visible at the top of frame, perfectly still. Her lips are slightly parted -- she is silently praying while she works. Three-quarter view, looking down at the stone, not at the camera. Mid-morning light, diffuse and warm, no harsh shadows. No wind in the palms." \
  "the stillness of a windless Delta morning; quiet prayer without expectation"

###############################################################################
# 14. The Neighbour's Boy in the Lane -- cp_layla.14
###############################################################################
run_one "cp_layla_neighbours_boy" \
  "The Neighbour's Boy in the Lane" \
  "A small boy cries alone in the dust of the village lane; Layla, hands still floured from dough, steps to the doorway so he can see a face" \
  "Layla stands just inside the doorway of her mud-brick house, one hand on the wooden doorframe. Her hands are dusted white with flour from dough she has left inside on the flat stone. In the middle distance of the narrow village lane, a small boy (about three years old, simple grey gallabiya, bare feet) sits in the dust of the lane crying, his face turned up toward Layla's doorway. His mother is not in frame. Other house doors along the lane are shut. Late morning light, harsh sun on the dust of the lane, but Layla's doorway is in deep cool shadow. Layla's face is not comforting or smiling -- it is steady, present, witnessing. Her body is still; she does not step out into the lane. The viewer sees both figures in the same frame: Layla in shadow in the foreground left, the boy in sunlight in the middle distance." \
  "the restraint of being a good neighbour; presence as a form of care; being seen as enough"

###############################################################################
# 15. Her Mother's Left Hand -- cp_layla.15
###############################################################################
run_one "cp_layla_mothers_hand" \
  "Her Mother's Left Hand" \
  "Layla notices, mid-meal, that she has begun to reach for bread with her left hand -- the way her dead mother always did" \
  "Close-medium interior shot of Layla sitting cross-legged on a worn woven mat inside her mud-brick house. A low wooden tray in front of her holds a small broken piece of aish baladi (flat Egyptian bread) and a shallow clay bowl of ful medames (brown stewed beans). Layla is in the middle of lifting a piece of the bread toward her mouth with her LEFT hand -- this left-handedness is the single most important visual detail and must read clearly. Her right hand is busy in her lap, adjusting a seam of her headscarf. Her gaze is distant, not at the food, not at the camera -- somewhere inward. The light is soft, single-source, from a wooden-lattice window off-frame right, casting a patterned shadow on the packed-earth floor. A single hen stands at the edge of the mat in the background, incurious. The interior is spare: a clay water-jar in one corner, a low wooden chest against the far wall. Palette is warm ochre, cream, the deep brown of the bread." \
  "the private grief of noticing you have become your mother; inheritance as gesture, not story"

echo "[$(date +%H:%M:%S)] all done"
