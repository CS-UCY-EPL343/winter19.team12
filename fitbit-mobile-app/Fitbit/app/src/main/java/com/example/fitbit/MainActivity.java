package com.example.fitbit;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.ConnectivityManager;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.Button;

import com.example.fitbit.model.User;

import java.util.HashMap;
import java.util.Map;

@SuppressLint("SetJavaScriptEnabled")
public class MainActivity extends AppCompatActivity {
    public static final String GRAPH_ENDPOINT = "/live_graph";
    public static final boolean GENERATE_DUMMY_VALUES = false;//if true,dummy metrics are sent to the server
    private NetworkChangeReceiver mNetworkReceiver;
    private static DummyLooper dummyLooper;
    private static MetricStorageManager metricMgr;
    private WebView mWebView;

    private void logout() {
        User.deleteAll(User.class);
        if (GENERATE_DUMMY_VALUES) {
            dummyLooper.stop();
        }
        if (metricMgr != null) {
            metricMgr.stop();
        }
        Intent myIntent = new Intent(MainActivity.this, LoginActivity.class);
        startActivity(myIntent);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        unregisterReceiver(mNetworkReceiver);
        stopService(new Intent(this, CollectDataService.class));
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        IntentFilter intentFilter = new IntentFilter();
        intentFilter.addAction(ConnectivityManager.CONNECTIVITY_ACTION);
        mNetworkReceiver = new NetworkChangeReceiver();
        registerReceiver(mNetworkReceiver, intentFilter);
        setContentView(R.layout.activity_main);
        mWebView = (WebView) findViewById(R.id.graph_webview);
        mWebView.getSettings().setJavaScriptEnabled(true);
        Map<String, String> headers = new HashMap<String, String>();
        Log.d("TOKEN", User.first(User.class).getToken());
        headers.put("Authorization", "Bearer " + User.first(User.class).getToken());
        mWebView.loadUrl(Urls.SERVER_URL + GRAPH_ENDPOINT, headers);
        MetricStorageManager metricMgr = new MetricStorageManager();
        metricMgr.start();
        if (GENERATE_DUMMY_VALUES) {
            dummyLooper = new DummyLooper();
            dummyLooper.start();
        }
        startService(new Intent(this, CollectDataService.class));
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.menu, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle item selection
        switch (item.getItemId()) {
            case R.id.edit_profile_menu:
                startActivity(new Intent(MainActivity.this, EditProfile.class));
                return true;
            case R.id.logout_menu:
                logout();
                return true;
            case R.id.change_password:
                startActivity(new Intent(MainActivity.this, ChangePasswordActivity.class));
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }

}
