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


###############################################################################
# TIER 2 -- law-reaction beats (prompt specs in prompts/catalog.md)
###############################################################################

run_one "cp_layla_column_returns" \
  "The Column Returns" \
  "Ahmed has come home from the war, thinner, in the doorway, deciding whether he is still permitted to cross the threshold" \
  "Interior of a Lower Egyptian village mud-brick house, afternoon light. Ahmed (late 20s to 30s, thin, tired, scruffy beard, dusty grey gallabiya, a worn bundle at his feet) stands in the open doorway. Layla (early 30s, headscarf, composed) is at the low table; she has just put down a piece of bread. They are NOT touching; they are looking at each other across the small room. Afternoon light slanting in from outside behind him, silhouetting his outline. Three-quarter composition, both in frame." \
  "the husband is not entirely the husband she sent away, and she does not mind"

run_one "cp_layla_clerks_letter" \
  "The Clerk's Letter" \
  "an official on a donkey has come through the village with a ledger and a list of names; he has one name for Layla's house" \
  "Village lane outside a mud-brick house. An official (man in formal dark robes, tarboosh, tired face, no warmth) sits on a donkey with a ledger open across the saddle. He is reading from it. In the foreground doorway, Layla (early 30s, headscarf) stands with her hand on the doorframe. Behind her, at a respectful distance in the lane, five or six village women gathered, watching, not close. Mid-morning light. She is not yet weeping; her face is composed." \
  "the news delivered like a parcel; the weeping is for later"

run_one "cp_layla_shutters" \
  "The Shutters Close" \
  "a revolution has begun in the country; Layla bolts the shutters of her house, a strip of late afternoon light reduced to a line" \
  "Interior of a mud-brick house, late afternoon. Layla (middle-aged) bolts the wooden shutter of a small window from inside. Between the two shutters, a narrow vertical strip of outside light cuts a line across her face. Through the sliver: dust rising in the lane, suggestion of horses or a crowd (not rendered in detail). Interior otherwise dim. Her expression is set, unafraid, focused." \
  "the house learning again what it means to be shut"

run_one "cp_layla_first_envelope" \
  "The First Envelope" \
  "the country has handed something directly to her for the first time — a brown envelope with her name" \
  "Outside a mud-brick or tenement doorway, late morning. Layla (middle-aged or older, headscarf) seated on the threshold step, a plain brown envelope held in both hands in her lap. She is looking at it, not at the camera. A clerk (man in dark jacket) is a few steps down the lane, moving on to the next house. A neighbour woman across the lane watches from her own doorway. Warm light." \
  "the country has, at last, handed a thing directly to her"

run_one "cp_layla_women_fields" \
  "The Law Catches Up to Us" \
  "the law has formally recognised that women work the fields; Layla at the edge of a field with another woman beside her" \
  "Edge of a cotton or wheat field in Lower Egypt at morning. Layla (mid-life, headscarf, working dress) and another village woman (similar age, simpler headscarf) are working the furrow side by side — bent over, hands in the soil, sleeves pushed up. Soft morning light, long shadows. Both women looking down at the work, not at the camera. A donkey in the far distance. The composition emphasises the two women as peers, working together openly." \
  "the law coughing and noticing work that was always being done"

run_one "cp_layla_women_hiring" \
  "They Are Hiring Women Now" \
  "three women of the lane walk away toward the distant mill gate with lunch pails; Layla stands at her doorway, not following, yet" \
  "Village lane corner in late morning. In the middle distance, three women (headscarves, modest working dresses, early middle-aged) walk away down a dirt track toward a distant mill building on the horizon; each carries a small tin lunch pail. In the foreground, Layla (headscarf, apron, middle-aged) stands leaning in her doorway, watching them go. Her expression: attentive, considering, neither joyful nor sad. Morning light." \
  "the door has opened and she is, this morning, standing in the doorframe"

run_one "cp_layla_on_rolls" \
  "I Am on the Rolls" \
  "Layla signs a voter-roll at a small district office counter; a clerk stamps a paper; other women wait behind her" \
  "Small rural district office interior. Layla (middle-aged) at a wooden counter, a pencil in her hand, signing a lined voter-roll book that is open on the counter before her. A young clerk (dark jacket, small moustache) stamps a paper beside her with a wooden stamp. Behind Layla, three or four other women wait in line. Flat indoor light from a single high window. The mood is mundane-historic; nobody is smiling." \
  "the flat mundane historic weight of being listed"

run_one "cp_layla_school_built" \
  "A School in the Next Village" \
  "a new whitewashed one-room schoolhouse has been built in the next village; boys and one girl are entering" \
  "Dusty road between two villages. In the middle distance: a newly whitewashed small one-room schoolhouse with a tiled roof, a painted sign in Arabic above its door. A few village boys (7-11 years old) and one girl (same age range) walk toward the door, each with a small slate. In the foreground across the road, Layla (middle-aged) stands watching, basket on her hip. Morning light, the whitewash of the school almost glowing against the ochre of the road." \
  "the building is small; the consequences will not be"

run_one "cp_layla_children_school" \
  "They Will Be Taken to the School" \
  "Layla stands in her doorway; her daughter and other village children are walking down the lane toward the schoolhouse, slates in hand" \
  "Village lane mid-morning. In the foreground doorway, Layla (middle-aged, headscarf) stands with her hand on the doorframe, watching. In the middle distance of the lane, a loose group of village children (mix of boys and girls, 7-10 years old) walk away toward the schoolhouse; each carries a small slate. Her daughter Nūr (9 years old, headscarf, serious expression) is at the front of the group, turning her head back once to look at Layla. Warm light." \
  "the permission she had not known she wanted"

run_one "cp_layla_coptic_neighbour" \
  "The Coptic Neighbour Exhales" \
  "Layla and Um Yusuf, her Coptic neighbour, sit together in a courtyard with tea; neither speaks; Um Yusuf's shoulders have gone down" \
  "Small mud-brick courtyard late afternoon. Two middle-aged women seated on low stools facing each other across a small wooden tray with two glasses of tea. On the left, Layla (headscarf of simple pattern, Muslim). On the right, Um Yusuf (simpler dark shawl-style headscarf, a small cross on a cord at her throat, slightly softer posture). Both hold their tea glasses; neither is speaking. Warm late-afternoon slanting light. The composition is intimate, companionable." \
  "a shoulder going down, quietly, in company"

run_one "cp_layla_procession" \
  "The Procession Passes" \
  "a small Coptic procession turns the corner in the village market and passes without catcalls or stones; Layla watches from a vegetable cart" \
  "Village market. In the middle distance turning a corner: a small Coptic procession — a priest in black robes and tall headdress, two young boys in white surplices carrying tall candles, a man carrying a painted wooden icon on a board. In the foreground at a vegetable cart, Layla (middle-aged, headscarf) stands with her fingers on a cucumber, watching them pass. The vegetable-seller also watches. No stones; no shouting. Late morning light." \
  "the small shock of a thing happening without reprisal"

run_one "cp_layla_children_leave" \
  "The Children Leave the Floor" \
  "the factory foreman has been ordered to send all children under twelve home; a loose cluster of small children walk out past him" \
  "Factory doorway, exterior shot. A foreman (middle-aged man, dark jacket, short moustache, tired face) stands with a paper in his hand by the open factory door. A loose cluster of small children (ages 8-12, both boys and girls, thin, dusty working clothes) walk out past him into bright morning daylight. In the foreground, Layla (middle-aged, headscarf) stands holding a cloth-wrapped bundle of bread, watching them pass. A boy of ten walks past her receiving a piece of the bread from her hand. The mood: a mercy that costs something." \
  "a mercy that has, for a household, a cost"

run_one "cp_layla_mosque_doctor" \
  "The Doctor at the Mosque" \
  "a charitable physician sees patients in the courtyard of the village mosque on Fridays" \
  "Courtyard of a small village mosque, Friday afternoon. A young physician (clean white shirt, no European hat — a modest Egyptian doctor, perhaps a tarboosh, mid-30s) examines an elderly woman seated on a stool; he has a small leather bag of instruments beside him. Along the mosque wall, a line of waiting patients sits on benches in the shade — including Layla (middle-aged) in the foreground waiting her turn. Warm light, columns of the mosque's arcade visible. Simple, respectful composition." \
  "mercy organised through the mosque, not yet through the state"

run_one "cp_layla_next_village_doctor" \
  "The Doctor in the Next Village" \
  "Layla walks four miles with a sick uncle to a newly-built small clinic where the state pays the doctor" \
  "Exterior of a small newly-built single-storey clinic building on the edge of a neighbouring village. Morning light. In the foreground, Layla (middle-aged, headscarf, tired) walks toward the clinic door supporting an elderly man (Uncle Khaled — thin, stooped, simple gallabiya, scarf at his neck). The clinic has a small painted sign in Arabic over the door. Dust road. No crowd; just the two of them, arriving." \
  "a state has, for once, placed something useful within walking distance"

run_one "cp_layla_guard" \
  "The Guard Has Been Installed" \
  "a new metal safety guard covers the rotating leather belt of a textile machine in the mill; two workers examine it" \
  "Interior of a textile mill, shafts of dusty light through high windows. A new metal safety guard (painted grey-green) has been fitted over the rotating leather belt and pulleys of a textile loom. Two working men in overalls examine the guard — one is Ahmed (early 40s, tired face, bearded). Machinery visible behind them. Industrial register: oil, dust, fabric lint in the air." \
  "the metal that was supposed to be there all along"

run_one "cp_layla_meeting" \
  "The Meeting After Shift" \
  "a dozen workers meet legally for the first time in a room above a coffeehouse, after the shift; a speaker at the head of a long table" \
  "Small room above a coffeehouse, evening lamplight from two hanging oil lamps. A dozen working men in simple jackets, caps, and working clothes seated along a long wooden table. At the head of the table stands a man making a small gesture as he speaks. Ahmed (early 40s) seated at the middle of the table. In the doorway at the back: Layla (middle-aged, headscarf), standing just inside, witnessing. The mood: earnest, intent, NOT revolutionary, professional. Warm lamplight." \
  "the first legal gathering of men who had been gathering illegally"

run_one "cp_layla_strike" \
  "The Strike" \
  "a crowd of workers at the mill gate with a hand-painted banner; police on the opposite side of the street, not yet advancing; Layla in the crowd with a basket of bread" \
  "Outside the iron gate of a textile mill, morning. A crowd of perhaps thirty working men standing in front of the gate; two of them hold up a hand-painted cloth banner with Arabic script. Across the street, four policemen in dark uniforms stand in a loose group, not advancing. In the foreground, Layla (middle-aged, headscarf) is visible in the crowd with a basket of bread on her hip, handing a loaf to a short man with a clipped moustache who is doing a small hopping step of excitement at the end of the banner. Tense but not yet violent." \
  "the air before anything breaks; a crowd, a banner, a decision pending"

run_one "cp_layla_minaret_silence" \
  "The Minaret's Silence" \
  "it is the exact hour of the call to prayer, and the call does not come; Layla pauses over her work in the courtyard" \
  "Small mud-brick courtyard, sharp noon light. Layla (middle-aged, headscarf) pauses mid-motion at the stove, a wooden spoon still in her hand; her head is slightly tilted, listening. Her youngest child (ages 5-7) stands in the doorway of the house behind her, watching her stillness. A minaret is visible rising above the palm-fronds in the far distance over the courtyard wall. Dead still air. Dust hanging motionless. Her face: the absence of an expected sound registered as a small, serious question." \
  "the absence of a sound one had measured one's days by"

run_one "cp_layla_burning_letters" \
  "The Letter That Should Not Have Been Written" \
  "Layla at the stove feeding folded letters into the fire one by one; the baker's wife sits mute on the bench behind her" \
  "Interior of a small mud-brick kitchen, morning. Layla (middle-aged, headscarf, set face) kneels at an open clay stove, feeding a folded paper letter into the low flames. A small stack of other folded letters sits on the hearth-stone beside her, waiting. Behind her on a low wooden bench sits another woman (the baker's wife — Um Rashid, older, black mourning-style shawl, stricken face, not speaking). A cup of flour on the table, knocked slightly sideways. Cool morning light. No dramatic emotion — grim, deliberate." \
  "the specific morning on which memory becomes contraband"

run_one "cp_layla_station" \
  "The Station in the Lane" \
  "a newly-whitewashed police station has appeared at a corner of the lane with a blue lamp over the door; Layla passes with a basket" \
  "Village lane late afternoon. At the corner where the donkey-cart used to park: a newly-whitewashed brick building, fresh paint, with a single small blue lamp hanging above the door. A policeman in a new uniform stands at the step, hands clasped behind his back. In the foreground walking past on the lane, Layla (middle-aged, headscarf, basket on her hip) has her head slightly lowered and her pace even. She is not looking at the station. She is walking by." \
  "the blue lamp does not ask after her"


###############################################################################
# TIER 3 -- technology arrivals + market-goods pulses
###############################################################################

run_one "cp_layla_railway" \
  "The Iron Horse" \
  "the first railway passes the village on a new embankment; villagers watch" \
  "A small knot of village people (men in gallabiyas, women in headscarves, a few children) stand on a low dirt rise in Lower Egypt, shading their eyes, watching a steam locomotive pulling three carriages move across a new railway embankment in the middle distance. A plume of white steam. Layla (middle-aged) in the foreground, shading her eyes with one hand. Ochre landscape, palm trees, midday light. The train is the only modern thing in frame." \
  "an iron thing in the landscape that is not a camel"

run_one "cp_layla_telegraph" \
  "A Word From Beyond" \
  "a village telegraph clerk reads a printed telegram aloud to Layla at a post-office counter" \
  "Interior of a very small rural post office. Behind a wooden counter: a clerk in a dark jacket and tarboosh reads from a long printed paper strip (a telegram). On the customer side: Layla (middle-aged) with her market basket, listening attentively, her lips slightly parted in bafflement. The telegraph apparatus on a shelf behind the clerk. Afternoon light through a small window." \
  "the strangeness of a sentence that has come without a body"

run_one "cp_layla_radio" \
  "Voices in the Air" \
  "an early 1930s wooden-cased radio on a shelf in a coffeehouse; men crowded around listening" \
  "Interior of an Egyptian coffeehouse, evening. On a high shelf: an early wooden-cased radio with a fabric speaker grille; its glass dial glowing faintly. Five or six men (gallabiyas, waistcoats, tarbooshes, varying ages) crowded around, heads tilted up toward the radio, listening. In the background doorway from the street: Layla (older, headscarf), standing just inside, also listening. Warm amber lamplight." \
  "the world speaking into a room where it has not previously spoken"

run_one "cp_layla_coffee" \
  "The Cup of Coffee" \
  "a small brass coffee cup on a table, steam rising; two hands — Layla's and another woman's — holding opposite cups" \
  "Overhead close-medium shot of a small wooden table with a tray. Two small ornate brass coffee cups with filigree holders, each with thin steam rising. Layla's hand (older, work-worn, headscarf edge visible) cupped around the near cup. Another woman's hand opposite (a neighbour, unseen face) around the far cup. Morning light, warm palette. The dark liquid visible in the cups. Intimate, still, quiet." \
  "the dark bean in the little cup"

run_one "cp_layla_sugar" \
  "The White Sugar" \
  "Layla pours a twist of paper containing refined white sugar into a clean glass jar in her kitchen" \
  "Interior of a mud-brick kitchen, midday. Layla (middle-aged, headscarf) at a low wooden bench pouring refined white sugar crystals from an opened paper twist into a clean glass jar. A teapot simmers on a small brazier in the background. Her expression is careful, faintly surprised by the whiteness. Warm earth-tone kitchen." \
  "a substance whiter than anything in her kitchen"

run_one "cp_layla_cloth" \
  "The Cloth from the Port" \
  "a bolt of blue printed European cotton on a market stall; Layla lifts a corner of it between two fingers" \
  "Fabric merchant's stall in an Egyptian market. A bolt of thin well-woven European printed cotton in a deep floral blue unfurled slightly on the wooden counter. Layla (middle-aged, headscarf) lifts a corner of the fabric between her thumb and forefinger, examining it. The merchant in the background blurred. Mid-morning light. Other bolts in various colours piled beside." \
  "the colours are not the colours the dyers of the village have"


###############################################################################
# Editor-audit additions -- new events cp_layla.83, .125-.128
###############################################################################

run_one "cp_layla_forty_days" \
  "The Forty Days" \
  "forty days after Layla's death; Um Yusuf brings flat mourning-bread; Nūr sits at the table writing a letter to Mariam in Cairo" \
  "Interior of Layla's kitchen — now hers only in memory. Morning light. Um Yusuf (elderly Coptic woman, darker shawl, simple cross at her throat) stands just inside the doorway carrying a cloth-wrapped bundle. At the low table, Nūr (a young woman in her early 20s, headscarf, inherited her mother's face) is writing a letter with pen and paper. On the shelf above the empty coat-hook: a small metal tobacco-tin sits where it has sat for twenty-eight years. Behind a loose brick in the wall (visible as a faint irregularity): a hint of a hidden pot. Quiet, dignified. Layla is NOT in frame. The kitchen remembers her." \
  "the life has been handed forward; the kitchen continues"

run_one "cp_layla_district_office" \
  "The District Office" \
  "Layla waits on a wooden bench in a provincial district office; a clerk at a distant desk does not look up" \
  "Interior of a dim provincial government office, late morning. In the foreground: Layla (middle-aged, headscarf, clean dress, a folded paper in her lap) seated on a hard wooden bench against a wall. Small high unwashed window lets in a shaft of dusty light. Halfway across the room, a clerk (man, worn dark jacket, small thin moustache, tired face) works at a ledger without looking up. Empty benches on either side of her. Flat administrative light. The mood is waiting that has become habitual." \
  "the tiredness is worse than cruelty; cruelty can be argued with, tiredness cannot"

run_one "cp_layla_imam_visit" \
  "The Imam's Visit" \
  "Sheikh Abdallah sits on a cushion in Layla's kitchen with a tea-glass held by the rim; fifteen minutes of visiting, no sermon" \
  "Interior of a modest mud-brick kitchen, Friday afternoon. On a low cushion: Sheikh Abdallah (elderly bearded imam, white turban wrapped around a red tarboosh-base, neat dark robe, dignified) holds a small glass of mint tea by the rim (never by the side), sipping slowly. Across the low table from him, Layla (middle-aged, headscarf) seated on her own cushion. No third figure. Warm afternoon light from a window. The composition is calm, conversational; neither is speaking. A small plate of dates on the tray between them." \
  "fifteen minutes of tea and no religious instruction"

run_one "cp_layla_small_victory" \
  "The Small Victory" \
  "the nephew Fawzi, visiting from Cairo in European dress, has slipped in the mud at the village well; Layla and Um Yusuf laugh" \
  "Village well in a courtyard. In the middle distance: a young man (Fawzi, mid-20s, fashionable European-cut Cairo jacket, bright tarboosh knocked off) has just fallen on the muddy patch beside the well, one leg bent beneath him, face caked with mud, his European shoe visible in the wet. The tarboosh lies three paces away. In the foreground, Layla (middle-aged, headscarf) and Um Yusuf (darker shawl, cross at her throat) grip each other's forearms, laughing helplessly, tears almost. Other women at the well in the background, smiling politely. Warm late-morning light. Joy, specifically." \
  "the week is better than the week was; the fall was magnificent; the boy was fine"

run_one "cp_layla_mariam_letter" \
  "Mariam Writes from Cairo" \
  "a letter from Mariam arrives from Cairo; Nūr reads it aloud to Layla; there is a sentence in the middle that makes Layla pause" \
  "Interior of a mud-brick house, evening. On the floor mat: Nūr (teenager or young woman, headscarf, serious face) sits cross-legged with an unfolded letter in her hand, reading aloud. Opposite her on a cushion: Layla (older, headscarf, elderly hands folded in lap), head slightly tilted, eyes inward, listening. The envelope lies open between them. A single oil lamp casts soft warm shadows. The composition emphasises Layla's listening face — the moment the sentence about Mariam's oud-playing has just been read." \
  "the world outside the kitchen, received without Layla's body leaving it"


###############################################################################
# TIER 4 -- rural / seasonal ambient pulses
###############################################################################

run_one "cp_layla_moment" \
  "A Moment" \
  "Layla alone at the doorway in late afternoon light, looking out at nothing in particular" \
  "Mud-brick house doorway, late afternoon slanting light. Layla (young woman, early to mid-20s, headscarf) stands just inside her doorway, one hand against the wooden jamb, looking out across the courtyard. Behind her on a low bench: a shallow clay bowl of lentils she has not finished sorting. Her expression: neither sorrowful nor happy — simply present, resting in a minute she did not know she needed. Warm ochre palette. No other figures." \
  "the minute-long pause in a day otherwise full"

run_one "cp_layla_letter_not_come" \
  "The Letter That Has Not Come" \
  "Layla at the low table, a folded letter from months ago in her hand; Ahmed's stool empty and pulled slightly out at the foreground right" \
  "Interior of a small mud-brick house, morning light from a single window at left. Layla (young, mid-20s, headscarf) sits at a low wooden table, a folded Arabic letter in her hand that is creased soft from re-reading. Beside her on the table: an empty space where a new letter would sit if one had come. Foreground right: Ahmed's low wooden stool, pulled slightly out from the table, empty. A shelf behind her holds a small metal tobacco-tin. Her gaze is on the letter, not at the camera. Quiet composition." \
  "the weight of an absence shaped like a letter"

run_one "cp_layla_walking_field" \
  "Walking the Field She Owns" \
  "Layla walks the border stones of her own dhurra field at dawn; a heron stands in the irrigation channel" \
  "Edge of a green dhurra (sorghum) field in Lower Egypt at first light. Layla (early 30s, headscarf loose at her shoulders, simple working dress) walks along a worn footpath beside a line of small border stones, her hand brushing the tops of the grain. In the middle distance, a white heron stands one-legged in the narrow irrigation channel. Long soft dawn shadows, pale gold light across the field. Palm trees on the horizon. Serene, private." \
  "the word 'mine' has not yet become comfortable in her mouth"

run_one "cp_layla_bey_eye" \
  "Under the Bey's Eye" \
  "Layla plaits a palm-frond basket in her doorway; in the middle distance, a mounted overseer rides past" \
  "Village lane under harsh midday sun. In the foreground, Layla (mid-20s, headscarf, working dress) sits on the threshold of her mud-brick house, hands plaiting a half-finished palm-frond basket in her lap. Her eyes are on the basket; they do not lift. In the middle distance, a mounted bey's overseer (man on a dark horse, dark jacket, tarboosh, leather crop) rides slowly past, his face turned toward her but not stopping. Dust. The village lane empty except for him. Tension without drama." \
  "the old discipline of not looking up"

run_one "cp_layla_hen" \
  "The Hen That Will Not Lay" \
  "Layla crouched in her courtyard, a red hen on her lap, checking its health; three other hens scratching nearby" \
  "Packed-earth courtyard of a mud-brick house, warm midday light. Layla (early to mid-30s, headscarf, apron) crouches on the ground with a reddish-brown hen cradled on her lap — the hen has pale feathers along its left wing. She examines the hen. Three other hens peck at scraps nearby; a shallow tin tray of grain on the ground. Her expression: the puzzled practical calculation of a woman considering whether to keep or cook the bird. Ochre palette." \
  "the small puzzled economics of a household"

run_one "cp_layla_merchants_scale" \
  "The Merchant's Scale" \
  "Layla at Abu Hassan's market stall watching him weigh onions on a brass balance; other women wait their turn" \
  "Village market stall. A brass two-pan balance on the wooden counter, onions in the pan being weighed. Behind the counter: Abu Hassan (middle-aged man, stutter suggested by his tense posture, tarboosh, waistcoat) avoiding Layla's gaze. In the foreground, Layla (early 30s, headscarf) stands with her hands on her hips, watching the scale intently. Two other village women wait a step behind her. Midday light, dust in the air." \
  "distrust of a scale that does not come out in her favour"

run_one "cp_layla_river_low" \
  "Friday, the River Low" \
  "Layla at the edge of a low Nile on a quiet Friday, sleeves rolled, looking at the exposed mud where water should be" \
  "Bank of the Nile in Lower Egypt at midday. The river is unusually low: wide bands of exposed pale cracked mud visible along the bank, beyond which the narrow band of water runs. Layla (mid-30s, headscarf, sleeves rolled to her forearms) stands alone at the edge of the exposed mud, looking out across the water. A few old men in gallabiyas gather further down the bank in conversation. Her expression: quiet alarm. Ochre palette." \
  "the slow alarm of a river that will not, this year, give what it should"

run_one "cp_layla_old_woman" \
  "The Old Woman Who Sees Through Walls" \
  "Layla leans in the doorway of a neighbour's house, speaking quietly to an ancient seated woman wrapped in dark shawls" \
  "Doorway of a neighbour's mud-brick house. In the dim interior, seated on a low wooden stool: an ancient woman (easily 85-90, deep-lined face, white hair under dark shawl, dark shawls layered around her shoulders) whose eyes are not focused on Layla but somewhere past her. Layla (middle-aged) stands at the doorway, leaning in, speaking quietly, her hand on the doorframe. Afternoon light outside, cool dimness inside. The old woman's weathered hands folded in her lap." \
  "the village keeps its own records through its old women"

run_one "cp_layla_bread_not_rise" \
  "The Bread That Did Not Rise" \
  "Layla at the flat stone, a lump of dense unrisen dough in her hands, face turned aside; a single hen looks on" \
  "Courtyard of a mud-brick house, morning. Layla (early 30s, headscarf, apron, flour on her forearms) stands at a low flat kneading stone holding up a lump of dense flat dough that has not risen — it is heavy, the colour of bruised cream, its surface pocked but not domed. She looks sideways, not at the dough, mouth pressed to a line. A single hen stands at the edge of the stone watching her, not scratching. Warm earth tones." \
  "the ordinary small failure that a household does not survive many of"

run_one "cp_layla_dust_on_water" \
  "Dust on the Water" \
  "Layla at the well drawing up a rope bucket; the water surface shows a visible dusty skim of sand" \
  "Village well. Layla (mid-30s, headscarf, sleeves rolled) has drawn up a rope-and-bucket, the wooden bucket now resting on the stone rim of the well. Visible in close-medium view: the surface of the water inside the bucket is dusty — a pale brown skim of fine sand across its top. Layla studies it, her hand on the rope. Midday light. Behind her the wall of another woman's courtyard." \
  "the kinds of small wrongnesses one learns to count"

run_one "cp_layla_brothers_letter" \
  "The Younger Brother's Letter" \
  "Layla holds a letter on her knee; the neighbour's literate boy reads it aloud, tracing the line with his finger" \
  "Interior of a mud-brick house, afternoon. Layla (early 30s, headscarf) sits on a low wooden bench, an unfolded handwritten Arabic letter resting on her knee. Beside her on the bench: a serious boy of about ten (the neighbour's son, simple grey gallabiya, concentrated expression) leans in with his finger on the line he is reading aloud. Layla is not looking at the letter; her face is turned slightly inward, listening. Warm lamplight." \
  "the humiliation and the gift of being read to"

run_one "cp_layla_mule" \
  "The Mule That Will Not Move" \
  "Layla and Ahmed on a dirt track with a loaded mule planted between them; hands on hips, halter tight" \
  "Dirt track in Lower Egypt, midday sun. A loaded mule (grey, stubborn posture, saddlebags heavy with bundles) stands planted in the middle of the path. On one side, Ahmed (late 20s, gallabiya, beard, hand firm on the halter, exasperated); on the other side, Layla (mid-20s, headscarf, hands on her hips, mouth a line that is almost but not quite a smile). Dust on their sandals. Palm trees in the distance." \
  "the domestic comedy of frustration"

run_one "cp_layla_ramadan" \
  "The First Day of Ramadan" \
  "Layla kneels on a prayer rug in her courtyard at dusk; a small tray of iftar dates and water waits beside her" \
  "Small mud-brick courtyard at dusk. Pink-orange sky overhead. Layla (early 30s, headscarf, modest dress) kneels on a worn prayer rug, hands raised palms-up in supplication, her eyes closed. Beside the rug on the packed earth: a small round tray with a few dates on it and a clay cup of water, waiting. Behind her, the mud wall of the courtyard. Soft evening light. Stillness." \
  "the first day's particular anticipation"

run_one "cp_layla_nile_rises" \
  "The Nile Rises" \
  "Layla and Ahmed on a low dike watching dark silt-rich water creep across a parched field; a neighbour waves from across the water" \
  "Rural Delta landscape, late afternoon. Layla (mid-30s, headscarf) and Ahmed (bearded, gallabiya) stand together on top of a low earthen dike looking out across a field where dark silt-heavy floodwater is creeping across the parched clay, filling it in ripples. In the far distance, across the water, another man stands on a dike waving one arm in greeting. The silt is the colour of strong tea. Golden-orange late light. Relief visible in their posture." \
  "the yearly relief of the flood arriving"

run_one "cp_layla_hajj" \
  "The Hajj Returnees" \
  "Layla at the edge of the lane watching a procession of returnees in white ihram enter the village; women with trays of sweets" \
  "Village lane, late morning. A small procession of pilgrims returning from the Hajj walks down the lane — three men wrapped in simple white ihram-cloth, tired but upright, faces weathered from the long journey. Women of the village line the sides of the lane, holding trays with dates and sweets, reaching out with their hands. In the foreground, Layla (middle-aged, headscarf) stands at the edge of the lane, her hand raised palm-up in a greeting of peace. Warm midday light." \
  "the village's small holiness when its pilgrims return"

run_one "cp_layla_midwife_lamp" \
  "The Midwife's Lamp" \
  "Layla holds a small oil lamp at night; the midwife Badr walks ahead of her down the lane to a doorway where a woman is labouring" \
  "Village lane deep in the night. Starlight above the palms. In the foreground, Layla (early 30s, headscarf, wrapped in a dark shawl) holds up a small clay oil lamp with a wick that she has just trimmed, its warm flame casting a small golden pool around them. Ahead of her walks Badr the midwife (older woman, bent slightly, dark shawl, worn leather bag). Further ahead, a small doorway glows faintly where a woman is labouring. Dark ochre and black palette with the lamp as the single warm point." \
  "the unspoken economy of women attending women"

run_one "cp_layla_dates" \
  "The Date Harvest" \
  "boys high in a palm beating dates onto cloths below; women in the courtyard sorting the good from the split" \
  "Village courtyard late autumn. A tall date palm rises in the center; two boys (10-12 years old, simple gallabiyas) are up in its crown with long poles, knocking down dates onto large cloths spread beneath. In the foreground, three women of different ages seated cross-legged on a large mat, sorting fallen dates into several baskets (good / split / soft / black-spotted). Layla (middle-aged) is one of them, her hands in the dates. Warm amber palette, long afternoon light. A contented industriousness." \
  "the year's last abundance"


###############################################################################
# TIER 5 -- conversation events (the Pasha fantasy, one image per cluster)
# All shot in Layla's kitchen at evening lamplight, older Layla, eyes inward.
# Register: contemplative, intimate, a woman preparing to go to Cairo in her mind.
###############################################################################

run_one "cp_conversation_audience" \
  "An Audience in Cairo (root)" \
  "older Layla in her kitchen at evening lamplight, a small brass coffee-cup in her hand, eyes unfocused, about to slip into the imagined palace" \
  "Interior of Layla's mud-brick kitchen, evening. Older Layla (50s, grey streaks at her temples, headscarf, lined face, dignified) seated on a low wooden stool at the low table. One hand cupped around a small brass coffee-cup that is still steaming. Her eyes unfocused, looking past the doorway into a middle distance that is NOT in the frame. An oil lamp on the table casts warm shadows. A bowl of dough rests on the table, partially worked. The kitchen is her own; everything in it she has placed herself. Introspective, still." \
  "the fantasy is about to begin; the kitchen knows"

run_one "cp_conversation_kitchen" \
  "The Kitchen Returns (closer)" \
  "the same kitchen; Layla setting the empty coffee-cup down; the fantasy has ended and the kitchen is again just the kitchen" \
  "Same mud-brick kitchen, same evening, slightly later. Older Layla (50s) sets an empty small brass coffee-cup down on the low wooden table. The oil lamp has burned lower; shadows softer. Her face has softened too — she has carried something through the fantasy and set it down. A palm-frond roof visible. The bowl of dough has been covered with a cloth. Quiet completion." \
  "carried something, set it down"

run_one "cp_conversation_land" \
  "The Land (topic opener)" \
  "Layla on an imagined long carpet in a palace, standing at its end, holding a folded ledger-paper of the field" \
  "Interior of a grand imagined palace reception hall rendered in her mind. A long deep-red carpet runs toward a distant figure (unseen) at the far end. Layla (middle-aged, modest dress, headscarf) stands alone at the near end of the carpet, a folded paper in her hand — a deed or ledger of her field. Her posture upright, uncertain. Tall columns suggested rather than detailed. Warm light from high imagined windows. Her face determined." \
  "the peasant woman has entered the palace of her imagination"

run_one "cp_conversation_ahmed" \
  "Ahmed (topic opener)" \
  "Layla on the imagined carpet mid-sentence, one hand at her throat, the edge of the Pasha's slippered feet at the frame" \
  "Imagined palace reception hall, long carpet. Layla (middle-aged, headscarf) stands mid-speech, her right hand raised to her throat in the gesture of a woman about to say a husband's name. At the very edge of the frame (lower right), the tips of a man's ornate slippers visible — suggesting the Pasha who is listening, without showing him. Warm palace light. Her face composed; the grief or the love she has come to speak is in her throat, not yet on her face." \
  "she has come to speak his name into a country that has not yet said it"

run_one "cp_conversation_children" \
  "The Children (topic opener)" \
  "Layla on the carpet counting off names on her fingers; a folded paper in her lap as she kneels or half-sits" \
  "Imagined palace hall, long carpet. Layla (middle-aged, headscarf, modest dress) stands at the near end of the carpet mid-gesture: her right hand raised with the fingers slightly splayed as if counting names, her left hand holding a small folded paper. Her face earnest; she is describing her children to a listener not in frame. Warm palace light. Dignified composition." \
  "she is naming the citizens the country has not seen"

run_one "cp_conversation_room" \
  "The Room (topic opener)" \
  "Layla describing her tenement room with small precise gestures like a draughtsman; hands drawing a square in the air" \
  "Imagined palace hall. Layla (middle-aged, slightly urban-softened dress, headscarf) stands on the carpet gesturing — both hands partially raised, shaping a small rectangular volume in the air before her as if describing a room's walls. Her face concentrated. Warm palace light. Behind her, the unreachable end of the carpet stretches." \
  "describing her city with the precision of a draughtsman"

run_one "cp_conversation_paper" \
  "The Paper (topic opener)" \
  "Layla holding up a folded deed into the imagined palace light; face grateful, wary" \
  "Imagined palace hall. Layla (middle-aged, headscarf) stands on the carpet holding up with both hands a folded paper — a deed, the official seal visible on its corner — toward the light from a high window. The paper catches the light. Her face tilted up toward it rather than toward the unseen Pasha. Quiet intensity. Warm palette." \
  "she has come to thank the paper's maker, and to ask if it will last"

run_one "cp_conversation_country" \
  "What I Think of the Country (topic opener)" \
  "Layla mid-argument, one hand up emphasizing a point, the other clenched at her side" \
  "Imagined palace hall. Layla (middle-aged, headscarf, working dress) stands on the carpet with her right hand raised in a small gesture of emphasis and her left hand clenched at her side. Her face is not angry — it is clear and direct, the face of a woman who has rehearsed a sentence she has never before been permitted to speak. Warm palace light. Posture upright." \
  "she has come to tell the country what the country has been doing to her"

run_one "cp_conversation_mill" \
  "The Mill (topic opener)" \
  "Layla miming the shape of a textile machine she has never operated; her hands tracing a rectangle in the air" \
  "Imagined palace hall. Layla (middle-aged or older, headscarf, somewhat urban dress) stands on the carpet with both hands raised, tracing in the air the rectangular outline of a loom or textile machine. Her face is explanatory, almost lecturing, but controlled. Warm palace light. A hint of industrial soot on her sleeve that she has not noticed." \
  "the woman who has not worked the machine has come to describe it"

run_one "cp_conversation_small" \
  "A Small Thing (topic opener)" \
  "Layla on the carpet, her eyes on the carpet's pattern; nothing to say tonight, but she has come anyway" \
  "Imagined palace hall. Layla (older, headscarf, modest dress) stands at the near end of the carpet, her eyes cast downward to study the intricate red-and-gold pattern beneath her feet. Her hands are clasped loosely at her waist. The carpet's pattern is in clearer focus than the unreachable far end. Her face contemplative; she has come without a speech tonight. Soft palace light." \
  "she has nothing of weight to say tonight; she has come anyway"

run_one "cp_conversation_distance" \
  "The Distance (topic opener)" \
  "Layla in matriarch's clothes, hands folded, a small brooch at her collar; her imagined self is prosperous, which surprises her" \
  "Imagined palace hall. Layla (older, 50s-60s, finer headscarf of thicker fabric, a small decorative brooch pinned at her collar, her dress of better cloth than she grew up in) stands on the carpet with her hands folded in front of her in the careful posture of a woman unsure whether she deserves the finery she is wearing. Her face uncertain — not proud, not apologetic. Warm palace light." \
  "the peasant woman has become something her mother would not have recognised"

run_one "cp_conversation_envelope" \
  "The Envelope (topic opener)" \
  "Layla producing a plain envelope from her sleeve at the start of her speech" \
  "Imagined palace hall. Layla (middle-aged or older, headscarf) stands on the carpet with her right hand drawing out from her sleeve a plain brown envelope — the first envelope the country ever gave her. She holds it up before her as evidence. Her face serious, testimonial. Warm palace light." \
  "she has brought the envelope to the man who decided the envelope should exist"

run_one "cp_conversation_rolls" \
  "The Rolls (topic opener)" \
  "Layla holding a blank voter-roll, tracing her own name across the top with a fingertip" \
  "Imagined palace hall. Layla (middle-aged or older, headscarf) stands on the carpet holding a sheet of paper — a blank voter-roll — in her left hand while her right index finger traces invisible letters across its top line as if writing her own name. Her face concentrated with a small private pride. Warm palace light." \
  "she has come to show him what the roll looked like with her name on it"

run_one "cp_conversation_stall" \
  "The Stall (topic opener)" \
  "Layla's hand sketching in the air the shape of a market-scale as she describes her stall" \
  "Imagined palace hall. Older Layla (50s or 60s, apron faintly visible under her better dress, headscarf) stands on the carpet with her right hand raised in an angular gesture — shaping in the air the outline of a brass balance-scale, her first stall-scale. Her face proud and defensive at once. Warm palace light." \
  "the shopkeeper has come to describe her shop to the man who could close it"

run_one "cp_conversation_nile" \
  "The Nile (topic opener)" \
  "Layla describing the flood-line with her hand, palm flat and horizontal" \
  "Imagined palace hall. Layla (middle-aged, headscarf, village dress) stands on the carpet with her right hand held out flat, palm down, horizontal — sweeping the air at waist height as if demonstrating the level of the flood. Her face reverent. Warm palace light with a slight shimmer like water near her hand." \
  "she has come to speak of the river as if the river were a person the country should respect"

run_one "cp_conversation_lost_child" \
  "The Lost Child (topic opener)" \
  "Layla's hand at her breastbone; her eyes down; she is about to say a child's name she has kept for forty years" \
  "Imagined palace hall, dimmer than usual — shadows longer. Layla (older, 60s, headscarf, modest dress) stands at the near end of the carpet with her right hand pressed flat against her own breastbone. Her eyes are downcast. No props in her hands. Her mouth slightly open around a word she has not yet said. Soft palace light, almost sepia." \
  "she has come tonight to say a name she has kept for forty years"

run_one "cp_conversation_school" \
  "The School (topic opener)" \
  "Layla holding an imagined letter at a reading distance; describing a daughter's handwriting" \
  "Imagined palace hall. Layla (older, headscarf, village-to-urban dress) stands on the carpet holding a folded paper out at a reading distance — the pose of a mother describing her daughter's handwriting. Her face softened by unexpected pride. Warm palace light. Her other hand lifted slightly as if tracing an alif in the air." \
  "she has come about the daughter who can, now, read"


###############################################################################
# TIER 6 -- remaining placeholder events (14 images)
###############################################################################

run_one "cp_layla_tax_collector" \
  "The Tax Collector" \
  "a clerk sits at Layla's wooden chest in the courtyard writing in a ledger; she stands to one side, hands folded" \
  "Packed-earth courtyard of a Lower Egyptian mud-brick house. A clerk (middle-aged man, dark formal jacket, tarboosh, tired face) sits on a low stool at Layla's wooden wedding chest, writing into a large open ledger with a reed pen. Beside the chest: an open coffer with a few coins. In the foreground, Layla (early 30s, headscarf, simple working dress) stands with her hands folded at her waist, her gaze on the ledger. Across the yard in shadow, Ahmed (bearded, gallabiya) watches with arms crossed. Harsh midday light, dust in the air." \
  "the state's hand in the household's accounts"

run_one "cp_layla_loaf" \
  "The Price of the Loaf" \
  "Layla at a baker's counter receiving a smaller loaf than usual for the same coin; other women in line behind her" \
  "Interior of a small village bakery. Warm wood counter dusted with flour. Hajj Rashid the baker (older man, white cap, apron) hands a loaf of aish baladi across the counter to Layla (mid-30s, headscarf, basket on her arm). The loaf is visibly smaller than it should be; his eyes avoid hers, quiet apology in his posture. A low round oven in the background; two other village women wait their turn in the background. Warm light from the oven casts amber tones." \
  "a tax that changes the shape of bread"

run_one "cp_layla_election_day" \
  "Election Day" \
  "a small polling station in a village hall; Layla stepping away from the ballot box with a private expression" \
  "Interior of a small rural polling station (village hall or converted schoolhouse). A wooden ballot box on a plain table; an election official (middle-aged man, modest dark jacket, tarboosh) seated behind it with a ledger. Layla (middle-aged, headscarf, best dress — clean but simple) is in the act of turning away from the ballot box, her hand still near the slot where her folded slip has just been dropped. Her expression is inward and mundane-historic; she is not smiling but her eyes are steady. Two other women wait their turn behind her. Flat daylight through a small window." \
  "the first vote; mundane and historic in equal parts"

run_one "cp_layla_foreman_runner" \
  "The Foreman's Runner" \
  "a young mill-boy at Layla's tenement doorway, cap in hand, unable to speak; Layla at the threshold already understanding" \
  "Exterior/interior threshold of a Cairo tenement apartment, grey morning light. A mill-boy (12-14 years old, thin, dusty working clothes, flat cap twisted in his hands) stands in the open doorway, his face empty of words. Opposite him in the doorway, Layla (middle-aged, headscarf, wiping her hands on an apron) has gone very still. Her expression: she has understood from his face before he has spoken. The stairwell of the tenement visible behind him. Cool desaturated palette; muted, grave." \
  "the accident has already happened; the news is the echo"

run_one "cp_layla_own_stall" \
  "Her Own Stall" \
  "Layla behind a new small market stall with vegetables, scale, and a battered tin box; customers in foreground" \
  "Morning market, bright ochre light. In the center foreground, Layla (middle-aged, headscarf, apron) stands behind a small rough wooden market stall of her own. On the stall: woven baskets of onions, cucumbers, a pyramid of eggplants, a small brass two-pan balance, a battered tin coin-box in the corner. She is wiping her hands on the apron, faintly proud, faintly nervous. A woman customer in the foreground examines the onions. Another stall and village lane visible behind. Warm palette." \
  "the stall is hers; the responsibility is entirely hers"

run_one "cp_layla_month_without" \
  "The Month Without" \
  "Layla kneels at a water-jar that is almost empty; the hearth is cold; a child sits in the corner" \
  "Interior of a modest tenement room, dim cold grey-blue morning light from a single window. Layla (middle-aged, headscarf, a worn shawl around her shoulders) kneels on the floor beside a tall clay water-jar, tilting it forward to reach the last of the water. Opposite her: a small cold hearth with the ashes from yesterday's fire but no new fire lit. In the far corner: a small child of 4-5 sits on a worn cushion, knees drawn up, watching. No other figures. Palette muted — cold ochre, ash grey, pale cream. Quiet want." \
  "the month that does not, this year, have what the previous months had"

run_one "cp_layla_not_on_deed" \
  "Her Name Is Not on the Deed" \
  "Layla sorting beans at the kitchen table, the deed unfolded between her hands, a child behind her reading over her shoulder" \
  "Interior of a mud-brick kitchen, late afternoon light. Layla (middle-aged, headscarf) seated on the floor mat at the low wooden table; her hands have paused over a spread of sorted and unsorted beans in front of her. Between her hands, unfolded on the table, is the deed paper for the field — with Ahmed's name visible on it in Arabic script. Behind her shoulder stands her daughter Nūr (early teenage, serious face, headscarf) also looking down at the deed, her finger about to point. Two small clay bowls of beans, one with weevilled beans set aside. Warm quiet palette." \
  "the field she walks is not the field her name walks"

run_one "cp_layla_daughter_reads" \
  "The Daughter Reads" \
  "Layla seated cross-legged on a mat with Nūr beside her; Nūr reads aloud from a letter; Layla has her hand at her own throat, eyes closed" \
  "Close-medium interior scene on a worn woven mat. On the left, Layla (middle-aged, headscarf) sits cross-legged, her right hand raised to her own throat, her eyes closed, her face softened by an emotion she is trying not to show. On the right beside her, Nūr (8-9 years old, small headscarf, serious concentration) holds an unfolded handwritten Arabic letter in her lap and reads aloud with one finger tracing the line. Soft single-source lamplight from an oil lamp on a low chest. Warm cream and amber palette. Intimate." \
  "the word on the page has entered the house via a child"

run_one "cp_layla_compound" \
  "The Compound on the Edge of the Village" \
  "a walled plantation compound at the edge of the village; Layla walks past on the road without turning her head" \
  "Rural road on the edge of a Lower Egyptian village in the heat of midday. On one side of the road: a high plaster-over-mud-brick wall topped with shards of broken pottery, a heavy iron gate set in it; through the gate's grille, the suggestion of bowed figures labouring in a sun-scorched yard beyond. On the road in the foreground, Layla (middle-aged, headscarf, water jar balanced on her shoulder) walks past the gate without turning her head, her eyes fixed on the road ahead. A few palm trees cast hard shadows. Harsh ochre light." \
  "the village's oldest shame in daily passing"

run_one "cp_layla_every_man" \
  "Every Man, They Say" \
  "a line of village men queued at a district registration office; Layla watches from outside with her daughter beside her" \
  "Dusty village main street in front of a small flat-roofed district office building. A long ragged line of village men (assorted ages, gallabiyas, fezes, tarbooshes, a few in European-cut jackets) waits to register at the open doorway where a clerk sits at a wooden table with an open ledger. Across the street in the foreground, Layla (middle-aged or older, headscarf) stands watching with Nūr (teenage, slightly shorter, also headscarf) beside her. Both of them watching, not entering. Warm midday light, dust haze." \
  "the word 'every' has a narrow reading and a wide one"

run_one "cp_layla_poster" \
  "The Poster on the Wall" \
  "Layla passes a freshly pasted single-party political poster on a whitewashed wall; two policemen stand nearby" \
  "Village main street, early afternoon. On a whitewashed mud-brick wall at the center of the frame: a large, freshly pasted political poster — single-party emblem, bold Arabic slogan, stark colour — still damp at its lower edge. In the middle distance, two policemen in dark uniforms stand near the poster, hands clasped behind their backs, watching the lane. In the foreground, Layla (middle-aged, headscarf, basket on her hip) walks past with her head slightly lowered, not stopping, her eyes on the path. Flat harsh light." \
  "a face she is expected to recognise on a wall she used to use for laundry"

run_one "cp_layla_insurance_man" \
  "The Man with the Bag" \
  "a European insurance salesman at Layla's doorway with leather bag and printed leaflet; she holds the leaflet at an angle, not understanding the French" \
  "Doorway of a modest Cairo tenement apartment, morning light. A European salesman (40s, neat brown suit, small bowler hat, leather satchel slung on his shoulder, printed leaflets in his hand) stands on the landing outside her door. He extends a leaflet toward Layla; she (middle-aged, headscarf, apron, wiping her hands) holds the leaflet at a tilt, examining the French-language text with the polite incomprehension of a woman who cannot read what she is holding. Her expression neither rude nor welcoming." \
  "a door opened to the wrong kind of help"

run_one "cp_layla_strangers" \
  "Strangers in the Lane" \
  "Layla on her doorstep holding a covered plate; a Syrian woman across the lane receives it" \
  "Narrow Egyptian village lane, warm late afternoon light. In the foreground on her doorstep: Layla (middle-aged, headscarf, simple village dress) extends both hands holding a small covered plate of bamya. Across the lane, a Syrian woman (early 30s, different headscarf of Levantine cut, more ornate embroidery on her dress) receives the plate with both hands, smiling a small modest smile. Between them: two small Syrian boys playing in the dust, paying no attention. Warm palette, dust in the air." \
  "a plate crossing a lane that has just become larger"

run_one "cp_layla_letter_folded" \
  "The Gate Closes" \
  "Layla at the low table, hands folded over an open letter from Beirut, the envelope beside it" \
  "Interior of a modest kitchen, flat late-morning light. Layla (older, headscarf, lined face) sits at the low wooden table. Her hands are folded motionless over an open handwritten Arabic letter that has been unfolded on the table in front of her. A torn-open envelope sits beside it, the Beirut postmark visible. Behind her, a drawer is slightly open, revealing a few other folded letters inside. Her face is composed and private; she is not weeping. Quiet palette." \
  "a letter folded into the smallest square"

echo "[$(date +%H:%M:%S)] all done"
