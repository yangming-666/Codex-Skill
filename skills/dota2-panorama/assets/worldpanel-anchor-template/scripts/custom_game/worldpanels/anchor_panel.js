(function () {
    var panel = $.GetContextPanel();
    var root = panel;
    var text = panel.FindChildTraverse("AnchorText");

    function getAlignSize(wp, targetPanel) {
        var data = wp && wp.data ? wp.data : null;
        var fixedW = data ? Number(data.worldpanel_fixed_width) : 0;
        var fixedH = data ? Number(data.worldpanel_fixed_height) : 0;
        if (fixedW > 0 && fixedH > 0) {
            return { w: fixedW, h: fixedH, mode: "fixed" };
        }

        var useDesired = !!(data && data.worldpanel_size_mode === "desired");
        var w = useDesired ? (targetPanel.desiredlayoutwidth || targetPanel.actuallayoutwidth || 0) : (targetPanel.actuallayoutwidth || 0);
        var h = useDesired ? (targetPanel.desiredlayoutheight || targetPanel.actuallayoutheight || 0) : (targetPanel.actuallayoutheight || 0);
        return { w: w, h: h, mode: useDesired ? "desired" : "actual" };
    }

    function init() {
        var data = panel.Data || {};
        var wp = panel.WorldPanel || {};

        if (root) {
            root.SetHasClass("Elite", data.variant === "elite");
        }
        if (text && data.text) {
            text.text = String(data.text);
        }

        if (data.debug_anchor) {
            var size = getAlignSize(wp, root || panel);
            $.Msg("[AnchorTemplate]",
                "mode=", size.mode,
                "w=", size.w,
                "h=", size.h,
                "hA=", wp.hAlign,
                "vA=", wp.vAlign);
        }
    }

    init();
})();
