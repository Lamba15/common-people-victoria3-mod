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

###############################################################################
# TIER 1 -- BIGGEST NARRATIVE MOMENTS (prompt specs in prompts/catalog.md)
###############################################################################

# cp_layla.50 -- "The Smoke Above the Palm" (first textile mill)
run_one "cp_layla_mill_smoke" \
  "The Smoke Above the Palm" \
  "the first textile mill has appeared on the horizon of Lower Egypt; Layla passes it on a road" \
  "Layla on a dirt road in Lower Egypt, mid-life (mid-30s), walking with a basket. In the middle distance past a cluster of palm trees: a tall new red-brick factory chimney with a perfectly straight pillar of white smoke rising from it. A low brick factory building at its base, iron gate. A few men in simple working clothes walking toward the gate in the middle distance. Morning light, long soft shadows. Layla is looking at the chimney, not at the camera. Three-quarter view. Palette: warm ochre earth, dusty palm-green, a smudge of grey-blue for the smoke. No celebration in her face; just attention." \
  "a new vertical element in a horizontal landscape; the ground vibrating slightly"

# cp_layla.70 -- "Cairo Is Calling" (migration crossroads)
run_one "cp_layla_cairo_calling" \
  "Cairo Is Calling" \
  "a letter has arrived from Cairo offering factory work; Layla and Ahmed sit with it at the low table" \
  "Interior of a modest mud-brick village house. Layla and Ahmed (both mid-30s to 40s) seated cross-legged at a low wooden table. On the table: an unfolded letter in Arabic with a printed letterhead, a folded printed ticket beside it. Warm afternoon light from an open doorway behind them, silhouetting the lane. Their faces are serious but not alarmed; they are considering. Layla's hand rests near the letter, not touching it yet. A small bundle of belongings is NOT packed; the floor is still their floor. Three-quarter composition, both in frame." \
  "a decision that will reshape the rest of their life; the gravity before the leap"

# cp_layla.72 -- "The Suitor" (daughter's marriage)
run_one "cp_layla_suitor" \
  "The Suitor" \
  "a suitor and his mother have come to ask for Layla's daughter's hand; they sit with trays of tea" \
  "Interior scene, warm lamplight. Layla (now older, 50s, grey at her temples) seated on a cushion on the left, her teenage daughter (about 17, same face as Layla's mother, dark hair) beside her. Opposite them: an older woman (the suitor's mother, in dignified dark clothes) and a young man in his early 20s (fez, simple jacket, hands folded on his knees). A low tray between them with small glasses of tea and a plate of sweets. The composition is formal, old-fashioned. No one is smiling; everyone is attentive. Evening light from an oil lamp. The daughter's eyes are on the tea tray; the young man's are on the daughter; Layla's are on the mother of the suitor, reading her." \
  "the family's oldest quiet negotiation; weight disguised as hospitality"

# cp_layla.73 -- "The Mill Closes" (downturn crossroads)
run_one "cp_layla_mill_closed" \
  "The Mill Closes" \
  "the Cairo mill where Ahmed works has just closed; workers stand in the yard with their tools" \
  "Outside a Cairo textile mill's iron gate, now chained. A handful of working men in dusty clothes stand around the mill yard, empty-handed. In the foreground, Layla (middle-aged, headscarf, careworn face) and Ahmed (grey-streaked beard, tired) stand together on the street outside the gate, looking at the chain. A lunch pail dangles from Ahmed's hand. Late morning light. Other workers' families appear in the far background, leaving. The mood is not panic; it is the composed silence of people who have been through this before." \
  "the whistle has stopped; the silence is the question"

# cp_layla.80 -- "The Last Morning" (her death)
run_one "cp_layla_last_morning" \
  "The Last Morning" \
  "Layla, elderly, lies on her bed one morning and does not get up; the morning has the quality of a morning that does not require her to make it go" \
  "An elderly Layla (70s, face lined, hair long grey) lies on a low bed in a small spare mud-brick room, a thin cotton blanket to her waist. Her eyes are closed; her hand is open and at rest on the blanket. A small clay water-jug on a stool beside the bed. A shaft of warm morning light falls across her chest through an open window onto a small courtyard. A single palm-frond leaf visible through the window. No other figures. She is not yet gone, but she is done. Close-medium shot. The palette is cream, pale ochre, the soft grey of her hair. Absolute quiet." \
  "the day will go on without her, the way days do"

# cp_layla.82 -- "The Child"
run_one "cp_layla_child_fever" \
  "The Child" \
  "a fever has taken one of Layla's children before dawn; she holds the small body" \
  "Dim interior at first light. Layla (mid-30s or 40s, weary) sits on a low bed or pallet, holding a small swaddled child (toddler or small) against her chest. The child is very still. Her face is turned down toward the child, her lips moving silently. A single oil lamp on a chest beside the bed has burned low. A window at the far wall shows the first grey of dawn. A neighbour woman asleep on a mat in the corner of the room. No visible weeping. The composition is close, intimate, reverent." \
  "the hour between the fever stopping and the lane waking up"

# cp_layla.94 -- "A Paper with My Name" (women_own_property)
run_one "cp_layla_paper_my_name" \
  "A Paper With My Name" \
  "the law has passed that lets women own property; Layla signs a deed with her own name for the first time" \
  "Interior: a village notary's bench. Layla (middle-aged) seated on a stool, a deed-paper unfolded before her on the wooden bench, her name inked at the top of the page in Arabic. The notary (older man in a tarboosh) stands on the other side with a pen-holder. Layla's teenage daughter stands behind her shoulder, looking over. Layla holds a pen in her hand, hovering above the signature line. Her face concentrated. Warm lamplight. The paper is the visual center of the image." \
  "the first time her name has been asked for by a paper that will keep it"

# cp_layla.103 -- "The Chains Are Cut" (slavery banned)
run_one "cp_layla_chains" \
  "The Chains Are Cut" \
  "slavery has been banned; a young woman walks free from the old plantation compound at the village edge" \
  "A walled plantation-compound on the edge of a Lower Egyptian village, with its gate standing open this morning. A young woman (early 20s, dark skin, plain shift, no shoes) walks out through the gate carrying a small bundle. In the foreground, Layla (middle-aged, headscarf, composed face) stands with her hands folded, watching the young woman pass. Middle distance: a few other freed workers leaving the compound. Morning light. No celebration; this is witness, not parade." \
  "a law's small visible consequence; the watcher knows what is being watched"

# cp_layla.116 -- "The Square Fills and Does Not Empty" (right of assembly)
run_one "cp_layla_square_fills" \
  "The Square Fills and Does Not Empty" \
  "the first legal demonstration in her city; two hundred people with a banner, and the cavalry has not come" \
  "A modest city square in 19th-century Egypt. In the middle of the square, a crowd of about 200 ordinary people (men and women in mixed local and urban dress) stand around a man on a low wooden cart speaking to them; a hand-painted cloth banner above the cart reads in Arabic script. The cavalry is NOT in the frame; the absence is important. In the upper-left foreground, Layla (middle-aged) stands at a second-floor window of a residential building, one hand on the frame, watching down into the square. Late afternoon light. Her face: attentive, still, uncertain." \
  "the square did not empty; the cavalry did not come; she stands at the window for an hour"

# cp_layla.120 -- "Rifles in the Square" (militarized police)
run_one "cp_layla_rifles" \
  "Rifles in the Square" \
  "the police now carry rifles on their shoulders; Layla crosses the market square with onions" \
  "A small city market square in the late 19th century. Two policemen in dark uniforms, tarbooshes, stand at the corner of the square against the wall of a small shop; each has a military rifle slung over his shoulder. In the foreground, Layla (now elderly, 60s, stooped slightly, grey hair at her temples) walks past them carrying a basket with onions visible at its top. Her shoulders are small; her eyes are on the path. A few other market-goers at the far side of the square are moving in silence. Flat afternoon light." \
  "a square that used to be for onions is, tonight, for rifles"

# cp_layla.123 -- "The Market Eats the Village" (laissez_faire)
run_one "cp_layla_factory_field" \
  "The Market Eats the Village" \
  "a French sugar company has fenced off the field across the canal; the village is becoming the factory's suburb" \
  "A rural Lower Egyptian landscape with a wire fence running across what was once a cotton field. Behind the fence: a tall red-brick factory chimney, rail sidings, a French-lettered wooden sign reading 'Compagnie Sucre et Engrais de la Basse-Egypte'. In front of the fence: the broken line of an old irrigation channel and the dry edge of the canal. In the foreground, Layla (middle-aged) and her literate teenage daughter stand side by side looking through the gap in the fence. Early evening light, long shadows. The daughter's finger half-raised as if translating the sign for her mother." \
  "the rhythm of the village has become the rhythm of a whistle"

# cp_layla.124 -- "The Ministry Comes for the Stall" (command economy)
run_one "cp_layla_ministry" \
  "The Ministry Comes for the Stall" \
  "a cooperative's clerk has papers for Layla's stall; she signs her own name for the first time in her life" \
  "A small vegetable stall on a city street: cucumbers, tomatoes, a few eggplants in baskets, a small brass scale, a battered tin coin-box. In the foreground, a European-style man (middle-aged, grey suit, tarboosh, clipboard) stands on the customers' side of the stall with a printed document. Layla (elderly, headscarf, lined face) stands on the seller's side, a simple pen in her right hand, the pen's nib hovering over the signature line. Her left hand steadies the paper. The clerk's face is neutral, respectful. Evening light. Other stalls of the market in the blurred far background." \
  "she signs her own name for the first time; the tin will not be hers tomorrow"

echo "[$(date +%H:%M:%S)] all done"
