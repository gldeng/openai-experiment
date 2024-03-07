# Logs:
# 12. Removed 128x128
# 13. Use simple base prompt and no extra desc
# 14. No reorg, simple prompt
# 15. Try Chartreux breed (which has short hair)
# 16. Base on 15, adding "with 4 legs on the floor"
# 17. Base on 16, removing mentioning of "128x128 grid"
# 18. Modified base prompt
# 19. Add Bengal as breed, and remove breed traits
export BASE_PROMPT="A simple pixel art image of a bengal cat in a natural sitting pose with 4 legs on the floor, facing directly at the viewer,"
export EXTRA_DESC=""
export DB_NAME=cat_samples_progressive_0306_19
export NO_REORG=1
export TRAITS_FILE="xibo's-6-traits.json"
# Comments:
# 12. Image quality not as ideal
# 13. No-Reorg didn't work
# 14. Seems ok
# 15. Seems better than 14 which is Siamese cat