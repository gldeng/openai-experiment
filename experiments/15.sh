# Logs:
# 12. Removed 128x128
# 13. Use simple base prompt and no extra desc
# 14. No reorg, simple prompt
# 15. Try Chartreux breed (which has short hair)
export BASE_PROMPT="A simple 128x128 grid pixel art image of a Chartreux cat in a natural sitting pose, facing directly at the viewer,"
export EXTRA_DESC=""
export DB_NAME=cat_samples_progressive_0305_15
export NO_REORG=1
export TRAITS_FILE="xibo's-6-traits.json"
# Comments:
# 12. Image quality not as ideal
# 13. No-Reorg didn't work
# 14. Seems ok
# 15. Seems better than 14 which is Siamese cat
