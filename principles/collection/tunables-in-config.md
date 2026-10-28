# Tunables in config

**Claim:** a value someone will set (a quota, a threshold, a price) lives in a configuration file, read at run time, and a value nobody has measured yet is tagged PROVISIONAL.

- **Grade:** convention, supported with caveat.
- **Evidence:** [against](../../evidence/file-structure/against.md) (configuration).
- **Check:** `provisional-tags`: a tag older than 90 days becomes a question; whether a value belongs in config is judgment.
- **Reader styles:** none override it.

## What it asks

- A value goes to config only when someone other than its author will set it, or will set it at a different time. Otherwise it is a named constant in the code.
- Every config value says what it controls and where its number came from.
- A guess is tagged PROVISIONAL, and the tag is removed only with a measurement.

## Why

A decision likely to change is hidden behind one place (Parnas 1972). Tagging a known shortcut is a studied practice:
self-admitted technical debt appeared in 2.4% to 31% of files in four projects (Potdar 2014).

## Limits

Every knob costs. Only 6.1% to 16.7% of parameters were set by most users and up to 54.1% were seldom set, and a
commercial system could drop 51.9% of its parameters (Xu 2015). Most real misconfigurations are parameter mistakes
(Yin 2011). Tags pile up: only 26.3% to 63.5% of tagged debt was later removed (Potdar 2014).
