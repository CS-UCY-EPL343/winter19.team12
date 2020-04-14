package com.example.fitbit;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;

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
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.fitbit.model.User;
import com.google.android.material.navigation.NavigationView;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.StringTokenizer;

@SuppressLint("SetJavaScriptEnabled")
public class MainActivity extends AppCompatActivity implements NavigationView.OnNavigationItemSelectedListener {
    public static final String GRAPH_ENDPOINT = "/live_graph";
    public static final boolean GENERATE_DUMMY_VALUES = true;//if true,dummy metrics are sent to the server
    private NetworkChangeReceiver mNetworkReceiver;
    private static DummyLooper dummyLooper;
    private static MetricStorageManager metricMgr;
    private WebView mWebView;
    private Map<String, String> headers = new HashMap<String, String>();

    private DrawerLayout drawerLayout;
    private void logout() {
        if (GENERATE_DUMMY_VALUES && dummyLooper!=null) {
            dummyLooper.stop();
        }
        if (metricMgr != null) {
            metricMgr.stop();
        }
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

    private void updateNavDrawer(){
        HashMap<String,String> headers = new HashMap<>();
        headers.put("Authorization", "Bearer " + User.first(User.class).getToken());
        CallAPI userInfo=new CallAPI("GET",headers,(r)->{
            Log.d("nav_drawer",r.toString());
            try {
                String res = "Welcome ";
                JSONObject results=new JSONObject(r);
                TextView welcomeTxt = (TextView)findViewById(R.id.welcome_user_txt);
                if(results.has("first_name")){
                    res+=results.getString("first_name")+" ";
                }
                if(results.has("last_name")){
                    res+=results.getString("last_name");
                    welcomeTxt.setText(res);
                }
                TextView emailTxt = (TextView)findViewById(R.id.email_txt);
                if(results.has("email")){
                    emailTxt.setText(results.getString("email"));
                }

            } catch (JSONException e) {
                e.printStackTrace();
            }

        });
        User currentUser=User.first(User.class);
        userInfo.execute(Urls.SERVER_URL+Urls.VIEW_PROFILE_DETAILS);

    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        IntentFilter intentFilter = new IntentFilter();
        intentFilter.addAction(ConnectivityManager.CONNECTIVITY_ACTION);
        mNetworkReceiver = new NetworkChangeReceiver();
        registerReceiver(mNetworkReceiver, intentFilter);
        setContentView(R.layout.activity_main);
        updateNavDrawer();
        Toolbar toolbar = findViewById(R.id.toolbar);
        toolbar.bringToFront();
        setSupportActionBar(toolbar);
        Objects.requireNonNull(getSupportActionBar()).setDisplayHomeAsUpEnabled(true);

        NavigationView navigationView = findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);
        navigationView.bringToFront();
        drawerLayout = findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(this,
                                                                 drawerLayout,
                                                                 toolbar,
                                                                 R.string.nav_open,
                                                                 R.string.nav_close);
        drawerLayout.addDrawerListener(toggle);
        toggle.syncState();
        mWebView = (WebView) findViewById(R.id.graph_webview);
        mWebView.getSettings().setJavaScriptEnabled(true);
        mWebView.getSettings().setDomStorageEnabled(true);

        Log.d("TOKEN", User.first(User.class).getToken());
        headers.put("Authorization", "Bearer " + User.first(User.class).getToken());
        mWebView.loadUrl(Urls.SERVER_URL + GRAPH_ENDPOINT, headers);


        MetricStorageManager metricMgr = new MetricStorageManager();
        metricMgr.start();
        if (GENERATE_DUMMY_VALUES){
            dummyLooper = new DummyLooper();
            dummyLooper.start();
        }
        startService(new Intent(this, CollectDataService.class));
    }

    @Override
    public void onBackPressed(){
        if(drawerLayout.isDrawerOpen(GravityCompat.START)){
            drawerLayout.closeDrawer(GravityCompat.START);
        }
        else{
            super.onBackPressed();
        }
    }

    @Override
    public boolean onNavigationItemSelected(@NonNull MenuItem item) {
        switch (item.getItemId()) {
            case R.id.nav_graph1:
                mWebView.loadUrl(Urls.SERVER_URL + GRAPH_ENDPOINT, headers);
                break;
            case R.id.edit_profile_menu:
                //TODO
                startActivity(new Intent(MainActivity.this, EditProfile.class));
                break;
            case R.id.change_password:
                //TODO
                startActivity(new Intent(MainActivity.this, ChangePasswordActivity.class));
                break;
            case R.id.logout_menu:
                //TODO
                logout();
                break;
            case R.id.nav_permissions:
                startActivity(new Intent(MainActivity.this,PermissionsActivity.class));
                break;
            case R.id.nav_history_calories :
                mWebView.loadUrl(Urls.SERVER_URL + GRAPH_ENDPOINT+"?type=2", headers);
                break;
            case R.id.nav_history_heartbeat :
                mWebView.loadUrl(Urls.SERVER_URL + GRAPH_ENDPOINT+"?type=3", headers);
                break;
            case R.id.nav_comparison :
                Log.d("test",headers.toString());
                mWebView.loadUrl(Urls.SERVER_URL + GRAPH_ENDPOINT+"?type=4", headers);
                break;
        }

        drawerLayout.closeDrawer(GravityCompat.START);
        return true;
    }

//    @Override
//    public boolean onOptionsItemSelected(MenuItem item) {
//        // Handle item selection
//        switch (item.getItemId()) {
//            case R.id.edit_profile_menu:
//                startActivity(new Intent(MainActivity.this, EditProfile.class));
//                return true;
//            case R.id.logout_menu:
//                logout();
//                return true;
//            case R.id.change_password:
//                startActivity(new Intent(MainActivity.this, ChangePasswordActivity.class));
//                return true;
//            default:
//                return super.onOptionsItemSelected(item);
//        }
//    }

}
