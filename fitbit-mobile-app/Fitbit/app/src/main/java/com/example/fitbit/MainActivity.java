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
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.Button;

import com.example.fitbit.model.User;

import java.util.HashMap;
import java.util.Map;

@SuppressLint("SetJavaScriptEnabled")
public class MainActivity extends AppCompatActivity {
    private Button mLogoutButton;
    public static final String GRAPH_ENDPOINT="/live_graph";
    private NetworkChangeReceiver mNetworkReceiver;
    private WebView mWebView;
    private void logout(){
        User.deleteAll(User.class);
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
        mLogoutButton = (Button)findViewById(R.id.logout_button);
        mLogoutButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                logout();
            }
        });
        mWebView = (WebView)findViewById(R.id.graph_webview);
        mWebView.getSettings().setJavaScriptEnabled(true);
        Map<String, String> headers = new HashMap<String, String>();
        Log.d("TOKEN",User.first(User.class).getToken());
        headers.put("Authorization","Bearer "+User.first(User.class).getToken());
        mWebView.loadUrl(Urls.SERVER_URL+GRAPH_ENDPOINT,headers);
        startService(new Intent(this, CollectDataService.class));
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.menu, menu);
        return true;
    }

}
