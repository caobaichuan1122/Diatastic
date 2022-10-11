(function (d, m) {
    var kommunicateSettings =
        { "appId": "16d104c5b45123a983a4e49c65eb3f22a", "popupWidget": true, "automaticChatOpenOnNavigation": true };
    var s = d.createElement("script"); s.type = "text/javascript"; s.async = true;
    s.src = "https://widget.kommunicate.io/v2/kommunicate.app";
    var h = d.getElementsByTagName("head")[0]; h.appendChild(s);
    window.kommunicate = m; m._globals = kommunicateSettings;
})(document, window.kommunicate || {});