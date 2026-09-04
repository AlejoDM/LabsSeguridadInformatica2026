#!/usr/bin/env bash
# check.sh — motor de verificación de retos por flags (SHA-256).
# El progreso se guarda en .progreso/<lab>.done (una flag-id por línea).
PROGRESS_DIR="${CTF_ROOT:-.}/.progreso"
_sha256() { printf '%s' "$1" | shasum -a 256 2>/dev/null | cut -d' ' -f1; }
_manifest_path() { printf '%s/retos.manifest' "$1"; }
_is_done() { local lab="$1" id="$2" f="$PROGRESS_DIR/$lab.done"; [ -f "$f" ] && grep -qx "$id" "$f"; }
_mark_done() { local lab="$1" id="$2" f="$PROGRESS_DIR/$lab.done"; mkdir -p "$PROGRESS_DIR"; _is_done "$lab" "$id" || echo "$id" >> "$f"; }

# ctf_submit <labdir> <lab-slug> <reto-id> <flag>
ctf_submit() {
  local dir="$1" lab="$2" id="$3" flag="$4"
  local manifest; manifest="$(_manifest_path "$dir")"
  [ -f "$manifest" ] || { ui_fail "No encuentro retos.manifest en $dir"; return 1; }
  local line expected got
  line="$(grep -E "^$id\|" "$manifest" | head -1)"
  [ -n "$line" ] || { ui_fail "No existe el reto '$id' en este lab."; ui_dim "Corré:  ./ctf status $lab"; return 1; }
  expected="$(echo "$line" | awk -F'|' '{print $3}' | tr -d ' ')"
  got="$(_sha256 "$flag")"
  if [ "$got" != "$expected" ] && [[ "$flag" != FLAG\{* ]]; then got="$(_sha256 "FLAG{$flag}")"; fi
  if [ "$got" = "$expected" ]; then
    if _is_done "$lab" "$id"; then
      ui_ok "Correcta (ya la tenías). Reto $id ✓"
    else
      _mark_done "$lab" "$id"
      source "$(dirname "${BASH_SOURCE[0]}")/banner.sh"; banner_victory
      ui_ok "Reto $id resuelto: $(echo "$line" | awk -F'|' '{print $2}')"
    fi
  else
    ui_fail "Flag incorrecta para el reto $id. Seguí investigando, loco."; return 1
  fi
}
# ctf_status <labdir> <lab-slug>
ctf_status() {
  local dir="$1" lab="$2"
  local manifest; manifest="$(_manifest_path "$dir")"
  [ -f "$manifest" ] || { ui_fail "No encuentro retos.manifest en $dir"; return 1; }
  local total=0 done=0 id titulo estado
  echo; ui_box "PROGRESO · LAB $lab"; echo
  while IFS='|' read -r id titulo _hash; do
    [ -z "$id" ] && continue; case "$id" in \#*) continue;; esac
    total=$((total+1))
    if _is_done "$lab" "$id"; then done=$((done+1)); printf '   %s✓%s  %-6s %s\n' "$C_GREEN" "$C_RESET" "$id" "$titulo"
    else printf '   %s·%s  %-6s %s%s%s\n' "$C_GREY" "$C_RESET" "$id" "$C_DIM" "$titulo" "$C_RESET"; fi
  done < "$manifest"
  echo; ui_bar "$done" "$total"; echo
  [ "$done" -eq "$total" ] && [ "$total" -gt 0 ] && ui_ok "¡Lab $lab COMPLETO! Ponete las pilas con la próxima unidad."
}
