"use strict";

function OnConfirmClicked() {
  GameEvents.SendCustomGameEventToServer("panorama_panel_confirm", {
    PlayerID: Players.GetLocalPlayer(),
  });
}

function OnServerMessage(data) {
  $.Msg("PanoramaPanel: server message", data);
}

(function () {
  const panel = $.GetContextPanel();
  panel.SetHasClass("Hidden", false);

  GameEvents.Subscribe("panorama_panel_message", OnServerMessage);
})();
