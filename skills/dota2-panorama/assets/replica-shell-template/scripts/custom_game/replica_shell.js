(function () {
    function cache(panel, id) {
        return panel ? panel.FindChildTraverse(id) : null;
    }

    function initReplicaShell() {
        var root = $.GetContextPanel();
        if (!root) return;
        cache(root, "ReplicaCanvas");
        cache(root, "ReplicaMainPanel");
        cache(root, "ReplicaSummary");
        cache(root, "ReplicaDamage");
        cache(root, "ReplicaRewards");
        cache(root, "ReplicaButtons");
    }

    initReplicaShell();
})();
