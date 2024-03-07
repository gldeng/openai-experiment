export OPENAI_API_KEY=<api key here>
export BASE_PROMPT="A simple 128x128 grid pixel art image of a Chartreux cat in a natural sitting pose with 4 legs on the ground, facing directly at the viewer,"
export EXTRA_DESC=""
export TRAITS_FILE="woody-5-traits.json" # save your json file and put the filename here
export NO_REORG=1

export DB_NAME="cat_samples_progressive_$(date '+%m%d')_$1_$2"
sdr sample-progressive $TRAITS_FILE -d $DB_NAME -p "$BASE_PROMPT" -e "$EXTRA_DESC" -R "$NO_REORG"
sdr generate -d $DB_NAME
sdr html -d $DB_NAME

# To use, save this script in a file, e.g. test.sh, then:
# source test.sh 1 01
# where first argument is the experiment number
# second argument is the trial number
# the filename will be cat_samples_progressive_MMDD_1_01.html