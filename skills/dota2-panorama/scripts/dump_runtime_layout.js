(function () {
    function round2(n) {
        return Math.round((Number(n) || 0) * 100) / 100;
    }

    function getRect(panel) {
        if (!panel) return null;
        return {
            id: String(panel.id || ""),
            classes: String(panel.GetAttributeString("class", "")),
            x: round2(panel.actualxoffset || panel.actuallayoutx || panel.actualx || 0),
            y: round2(panel.actualyoffset || panel.actuallayouty || panel.actualy || 0),
            width: round2(panel.actuallayoutwidth || panel.actualuiscale_x || panel.actualwidth || 0),
            height: round2(panel.actuallayoutheight || panel.actualuiscale_y || panel.actualheight || 0),
            visible: panel.visible === true
        };
    }

    function findBySelector(root, selector) {
        if (!root || !selector) return null;
        if (selector[0] === "#") {
            return root.FindChildTraverse(selector.slice(1));
        }
        if (selector[0] === ".") {
            var cls = selector.slice(1);
            return root.FindChildrenWithClassTraverse(cls)[0] || null;
        }
        return root.FindChildTraverse(selector);
    }

    function dumpLayout(rootSelector, selectors, eventName) {
        var root = $.GetContextPanel();
        if (rootSelector) {
            var maybe = findBySelector($.GetContextPanel(), rootSelector);
            if (maybe) root = maybe;
        }

        var rows = [];
        for (var i = 0; i < selectors.length; i++) {
            var sel = selectors[i];
            var panel = findBySelector(root, sel);
            rows.push({
                selector: sel,
                rect: getRect(panel)
            });
        }

        var payload = {
            root_selector: rootSelector || "",
            screen_w: Game.GetScreenWidth ? Game.GetScreenWidth() : 0,
            screen_h: Game.GetScreenHeight ? Game.GetScreenHeight() : 0,
            rows: rows
        };

        $.Msg("[ReplicaDump] " + JSON.stringify(payload));
        if (eventName) {
            GameEvents.SendCustomGameEventToServer(eventName, { payload: JSON.stringify(payload) });
        }
        return payload;
    }

    GameUI.ReplicaDumpLayout = dumpLayout;
})();
