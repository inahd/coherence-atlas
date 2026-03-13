#!/usr/bin/env bash

BASE="/opt/atlas"

echo "Installing full Nakshatra knowledge layer..."

mkdir -p $BASE/datasets
mkdir -p $BASE/graph

cat <<DATA > $BASE/datasets/nakshatra.yaml
Ashwini:
  deity: Ashwini Kumaras
  ruler: Ketu

Bharani:
  deity: Yama
  ruler: Venus

Krittika:
  deity: Agni
  ruler: Sun

Rohini:
  deity: Brahma
  ruler: Moon

Mrigashira:
  deity: Soma
  ruler: Mars

Ardra:
  deity: Rudra
  ruler: Rahu

Punarvasu:
  deity: Aditi
  ruler: Jupiter

Pushya:
  deity: Brihaspati
  ruler: Saturn

Ashlesha:
  deity: Nagas
  ruler: Mercury

Magha:
  deity: Pitrs
  ruler: Ketu

PurvaPhalguni:
  deity: Bhaga
  ruler: Venus

UttaraPhalguni:
  deity: Aryaman
  ruler: Sun

Hasta:
  deity: Savitar
  ruler: Moon

Chitra:
  deity: Vishvakarma
  ruler: Mars

Swati:
  deity: Vayu
  ruler: Rahu

Vishakha:
  deity: IndraAgni
  ruler: Jupiter

Anuradha:
  deity: Mitra
  ruler: Saturn

Jyeshtha:
  deity: Indra
  ruler: Mercury

Mula:
  deity: Nirriti
  ruler: Ketu

PurvaAshadha:
  deity: Apas
  ruler: Venus

UttaraAshadha:
  deity: Vishvadevas
  ruler: Sun

Shravana:
  deity: Vishnu
  ruler: Moon

Dhanishta:
  deity: Vasus
  ruler: Mars

Shatabhisha:
  deity: Varuna
  ruler: Rahu

PurvaBhadrapada:
  deity: AjaEkapada
  ruler: Jupiter

UttaraBhadrapada:
  deity: AhirBudhnya
  ruler: Saturn

Revati:
  deity: Pushan
  ruler: Mercury
DATA

echo "Nakshatra dataset installed."

echo
echo "Atlas now contains the full 27 Nakshatra system."

