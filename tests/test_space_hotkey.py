"""Tests for the optional `space_to_record` push-to-talk hotkey prop.

Phase 2 of PRD-35 adds a `space_to_record` boolean prop to
`AudioRecorderPolyfill`. When enabled, the component installs a global
window-level keyboard listener: holding `Space` starts recording, releasing
it stops. When focus is on an editable text field (input / textarea /
contenteditable), the hotkey MUST be suppressed so users can type a literal
space.

These tests exercise the generated React hook code (returned by
`add_hooks()`) for the presence/absence of:

  * A `keydown` AND `keyup` listener registered on `window`.
  * A guard that bails out when `document.activeElement` is an editable
    text field.
  * Cleanup via `removeEventListener` in the `useEffect` return.

The default (`space_to_record=False`) MUST emit none of the above, so
existing consumers stay byte-for-byte backward compatible.
"""

from __future__ import annotations

import pytest

from reflex_audio_capture import AudioRecorderPolyfill


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #


def _hooks_source(component: AudioRecorderPolyfill) -> str:
    """Return the concatenated JS source of all hooks emitted by `component`.

    `add_hooks()` returns a list of strings/Vars. We coerce each to `str` and
    join so the test can grep across the entire injected hook block.
    """

    return "\n".join(str(hook) for hook in component.add_hooks())


# --------------------------------------------------------------------------- #
# Backward compatibility                                                      #
# --------------------------------------------------------------------------- #


@pytest.mark.unit
def test_default_emits_no_global_keyboard_listener() -> None:
    """`space_to_record` defaults to False — no global key listener must be installed."""

    component = AudioRecorderPolyfill.create(id="default_recorder")
    src = _hooks_source(component)

    # No window-level keydown/keyup listener registration whatsoever.
    assert "addEventListener('keydown'" not in src
    assert 'addEventListener("keydown"' not in src
    assert "addEventListener('keyup'" not in src
    assert 'addEventListener("keyup"' not in src
    # No reference to the Space key.
    assert "' '" not in src or "Space" not in src  # belt and suspenders
    assert "Space" not in src


@pytest.mark.unit
def test_explicit_false_emits_no_global_keyboard_listener() -> None:
    """Passing `space_to_record=False` explicitly is also a no-op."""

    component = AudioRecorderPolyfill.create(
        id="explicit_false_recorder", space_to_record=False
    )
    src = _hooks_source(component)
    assert "Space" not in src
    assert "keydown" not in src
    assert "keyup" not in src


# --------------------------------------------------------------------------- #
# Enabled behavior                                                            #
# --------------------------------------------------------------------------- #


@pytest.mark.unit
def test_space_to_record_enables_global_keydown_keyup_listeners() -> None:
    """With `space_to_record=True`, both keydown AND keyup listeners are on window."""

    component = AudioRecorderPolyfill.create(
        id="ptt_recorder", space_to_record=True
    )
    src = _hooks_source(component)

    # Listeners are registered on window (or globally with `addEventListener`,
    # which when called bare in browser code targets `window`).
    assert "keydown" in src, "keydown listener missing when space_to_record=True"
    assert "keyup" in src, "keyup listener missing when space_to_record=True"

    # Must reference the Space key — either KeyboardEvent.code === 'Space'
    # or KeyboardEvent.key === ' '.
    assert (
        "'Space'" in src or '"Space"' in src or 'e.code' in src
    ), "no reference to the Space key in the hotkey hook"


@pytest.mark.unit
def test_space_to_record_suppresses_when_editable_field_focused() -> None:
    """The keydown handler must check `document.activeElement` for editable focus."""

    component = AudioRecorderPolyfill.create(
        id="ptt_focus_recorder", space_to_record=True
    )
    src = _hooks_source(component)

    # Focus-suppression: the listener must inspect document.activeElement.
    assert "document.activeElement" in src, (
        "focus-suppression check missing — keystroke must not toggle recording "
        "when an editable text field has focus"
    )
    # Must check at least one editable surface tag and contenteditable.
    lower = src.lower()
    assert "input" in lower
    assert "textarea" in lower
    assert "contenteditable" in lower


@pytest.mark.unit
def test_space_to_record_cleans_up_listeners_on_unmount() -> None:
    """The useEffect must return a cleanup that removes both listeners."""

    component = AudioRecorderPolyfill.create(
        id="ptt_cleanup_recorder", space_to_record=True
    )
    src = _hooks_source(component)

    assert "removeEventListener" in src, (
        "useEffect must return a cleanup that calls removeEventListener "
        "for both keydown and keyup to avoid leaking listeners on unmount"
    )


@pytest.mark.unit
def test_space_to_record_invokes_start_and_stop_refs() -> None:
    """keydown -> mediarecorder_start_<ref>(); keyup -> mediarecorder stop."""

    component = AudioRecorderPolyfill.create(
        id="ptt_dispatch_recorder", space_to_record=True
    )
    src = _hooks_source(component)
    ref = component.get_ref()

    # The start path uses the existing start ref the component already exposes.
    assert f"mediarecorder_start_{ref}" in src, (
        "keydown handler must call the existing start ref so behavior matches "
        "clicking the start button"
    )
    # The stop path stops the active mediarecorder ref (matching .stop() method).
    assert f"mediarecorder_{ref}" in src, (
        "keyup handler must reference the active mediarecorder ref to stop it"
    )
