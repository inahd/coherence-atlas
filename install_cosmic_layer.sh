#!/usr/bin/env bash

BASE="/opt/atlas/datasets"

echo "Installing cosmic ontology layer..."

mkdir -p $BASE

# Graha
cat <<DATA > $BASE/graha.yaml
Sun:
  type: graha
  qualities: authority, vitality

Moon:
  type: graha
  qualities: mind, emotion

Mars:
  type: graha
  qualities: energy, conflict

Mercury:
  type: graha
  qualities: intellect, speech

Jupiter:
  type: graha
  qualities: wisdom, expansion

Venus:
  type: graha
  qualities: beauty, pleasure

Saturn:
  type: graha
  qualities: discipline, restriction

Rahu:
  type: graha
  qualities: disruption, obsession

Ketu:
  type: graha
  qualities: detachment, liberation
DATA


# Rashi
cat <<DATA > $BASE/rashi.yaml
Aries:
  element: fire
  ruler: Mars

Taurus:
  element: earth
  ruler: Venus

Gemini:
  element: air
  ruler: Mercury

Cancer:
  element: water
  ruler: Moon

Leo:
  element: fire
  ruler: Sun

Virgo:
  element: earth
  ruler: Mercury

Libra:
  element: air
  ruler: Venus

Scorpio:
  element: water
  ruler: Mars

Sagittarius:
  element: fire
  ruler: Jupiter

Capricorn:
  element: earth
  ruler: Saturn

Aquarius:
  element: air
  ruler: Saturn

Pisces:
  element: water
  ruler: Jupiter
DATA


echo "Cosmic ontology installed."

echo
echo "Datasets now available:"
echo "  graha.yaml"
echo "  rashi.yaml"
echo "  nakshatra.yaml"

