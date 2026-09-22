#pragma once

// Custom code belongs on main only; never copy it into the oryx branch.
enum { CHAT_GAMING_LAYER = 1, CHAT_G2_LAYER = 2, CHAT_TYPING_LAYER = 3 };

static bool process_gaming_chat(uint16_t keycode, keyrecord_t *record) {
    // Consume the matching release even after switching layers.
    static bool consumed[MATRIX_ROWS][MATRIX_COLS];
    bool *pressed = &consumed[record->event.key.row][record->event.key.col];
    if (!record->event.pressed) {
        if (*pressed) {
            *pressed = false;
            return false;
        }
        return true;
    }

    uint8_t layer = get_highest_layer(layer_state);
    if (keycode == KC_F24 && layer == CHAT_G2_LAYER) {
        *pressed = true;
        tap_code(KC_ENTER);
        layer_move(CHAT_TYPING_LAYER);
        return false;
    }
    if (layer == CHAT_TYPING_LAYER &&
        (keycode == KC_ENTER || keycode == KC_ESCAPE)) {
        *pressed = true;
        tap_code(keycode);
        layer_move(CHAT_GAMING_LAYER);
        return false;
    }
    return true;
}
