package org.lg3as.admin;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

public class MainActivity extends Activity {
    private WebView wv;
    private boolean backOnce = false;

    /** Ouvre les liens externes (Telegram, navigateur) hors WebView. */
    private boolean openExternal(String url) {
        if (url == null) return false;
        if (url.startsWith("file:///android_asset/") || url.startsWith("about:")) return false;
        try {
            Uri u = Uri.parse(url);
            String host = u.getHost() != null ? u.getHost().toLowerCase() : "";
            if (host.equals("t.me") || host.endsWith(".t.me")) {
                String domain = "";
                if (u.getPathSegments() != null && !u.getPathSegments().isEmpty()) {
                    domain = u.getPathSegments().get(0);
                }
                if (!domain.isEmpty()) {
                    try {
                        startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse("tg://resolve?domain=" + domain)));
                        return true;
                    } catch (ActivityNotFoundException ignored) {
                        // Telegram absent -> repli https ci-dessous
                    }
                }
            }
            startActivity(new Intent(Intent.ACTION_VIEW, u));
            return true;
        } catch (ActivityNotFoundException e) {
            Toast.makeText(this, "Aucune application pour ouvrir ce lien", Toast.LENGTH_SHORT).show();
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        wv = new WebView(this);
        WebSettings s = wv.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setSupportMultipleWindows(true);
        wv.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                return openExternal(request.getUrl().toString());
            }

            @Override
            @SuppressWarnings("deprecation")
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                return openExternal(url);
            }
        });
        wv.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onCreateWindow(WebView view, boolean isDialog, boolean isUserGesture, Message resultMsg) {
                // target="_blank" -> ouvre hors WebView au lieu d'une fenetre invisible
                WebView.HitTestResult r = view.getHitTestResult();
                String url = r != null ? r.getExtra() : null;
                if (url != null && openExternal(url)) {
                    return false;
                }
                return super.onCreateWindow(view, isDialog, isUserGesture, resultMsg);
            }
        });
        setContentView(wv);
        // ECRAN : la WebView est réduite aux marges des barres système pour que
        // le contenu ne passe JAMAIS sous le poinçon caméra, les notifications,
        // la batterie/wifi (haut) ni la barre de navigation (bas). Fonctionne
        // sur tous les smartphones + à la rotation (nouveaux insets = relayout).
        try {
            getWindow().setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(0xFF000000));
            getWindow().setStatusBarColor(0xFF000000);
            getWindow().setNavigationBarColor(0xFF000000);
            android.view.View decor = getWindow().getDecorView();
            if (android.os.Build.VERSION.SDK_INT >= 30) {
                android.view.WindowInsetsController c = decor.getWindowInsetsController();
                if (c != null) { c.setAppearanceLightStatusBars(false); c.setAppearanceLightNavigationBars(false); }
            } else {
                int f = decor.getSystemUiVisibility();
                f &= ~(android.view.View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR | android.view.View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR);
                decor.setSystemUiVisibility(f);
            }
        } catch (Exception ignored) {}
        wv.setOnApplyWindowInsetsListener((v, insets) -> {
            try {
                android.view.ViewGroup.MarginLayoutParams lp =
                    (android.view.ViewGroup.MarginLayoutParams) v.getLayoutParams();
                lp.setMargins(
                    insets.getSystemWindowInsetLeft(),
                    insets.getSystemWindowInsetTop(),
                    insets.getSystemWindowInsetRight(),
                    insets.getSystemWindowInsetBottom());
                v.setLayoutParams(lp);
            } catch (Exception ignored) {}
            return insets.consumeSystemWindowInsets();
        });
        try { wv.requestApplyInsets(); } catch (Exception ignored) {}
        if (savedInstanceState != null) {
            wv.restoreState(savedInstanceState);
        } else {
            wv.loadUrl("file:///android_asset/www/index.html");
        }
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        wv.saveState(outState);
    }

    @Override
    public void onBackPressed() {
        if (wv != null && wv.canGoBack()) {
            wv.goBack();
            backOnce = false;
            return;
        }
        if (backOnce) {
            super.onBackPressed();
            return;
        }
        backOnce = true;
        Toast.makeText(this, "Appuie encore pour quitter", Toast.LENGTH_SHORT).show();
        new Handler(Looper.getMainLooper()).postDelayed(() -> backOnce = false, 2000);
    }
}
