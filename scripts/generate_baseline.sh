#!/usr/bin/env bash

BASE="/opt/atlas/datasets"

mkdir -p $BASE

cat <<EOF > $BASE/jyotish_core.yaml
graha:
  - Sun
  - Moon
  - Mars
  - Mercury
  - Jupiter
  - Venus
  - Saturn
  - Rahu
  - Ketu

rashi:
  - Aries
  - Taurus
  - Gemini
  - Cancer
  - Leo
  - Virgo
  - Libra
  - Scorpio
  - Sagittarius
  - Capricorn
  - Aquarius
  - Pisces

nakshatra:
  - Ashwini
  - Bharani
  - Krittika
  - Rohini
  - Mrigashira
  - Ardra
  - Punarvasu
  - Pushya
  - Ashlesha
  - Magha
  - Purva Phalguni
  - Uttara Phalguni
  - Hasta
  - Chitra
  - Swati
  - Vishakha
  - Anuradha
  - Jyeshtha
  - Mula
  - Purva Ashadha
  - Uttara Ashadha
  - Shravana
  - Dhanishta
  - Shatabhisha
  - Purva Bhadrapada
  - Uttara Bhadrapada
  - Revati

vedanta_schools:
  - Advaita
  - Visistadvaita
  - Dvaita
  - Acintya-bheda-abheda
EOF

echo "Baseline Vedic dataset created in /opt/atlas/datasets/"

