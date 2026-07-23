# Pending prod refresh

These 22 university thesis templates got the "unofficial / not affiliated" disclaimer
added to their source (2026-07). They are LIVE on letx.app but their prod preview + source
zip were NOT refreshed, because they do not build cleanly in a local TeX env (missing
fonts/figure assets/engine — e.g. mit/oxford need lualatex/xelatex + repo-vs-prod asset
drift). Per the gate rule "no unverified writes to a live download," refresh them on the
worker (full TeX Live + assets) during the next batch build, then update prod verified.

buet-thesis cambridge-thesis cuet-thesis du-thesis eth-thesis harvard-thesis iisc-thesis
iit-bombay-thesis iitd-thesis iitk-thesis iitm-thesis iut-thesis kuet-thesis mit-thesis
ntu-thesis nus-thesis oxford-thesis ruet-thesis stanford-thesis sust-thesis ucb-thesis
ut-thesis
