package com.example.fitbit;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.app.AlertDialog;
import org.json.*;

import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class LoginActivity extends Activity{
    public static final String LOGIN_ENDPOINT="/login_api";
    private Button mLoginBtn;
    private boolean loginSuccess=false;
    private EditText mPasswordInput,mUsernameInput;
    @Override
    public void onCreate(Bundle bundle){
        super.onCreate(bundle);
        setContentView(R.layout.login);
        mLoginBtn = (Button)findViewById(R.id.login_button);
        mUsernameInput = (EditText)findViewById(R.id.username_field);
        mPasswordInput = (EditText)findViewById(R.id.password_field);
        Log.d("TEST","mLoginBtn:"+mLoginBtn);
        mLoginBtn.setOnClickListener(new View.OnClickListener(){
            @Override
            public void  onClick(View v){
                handleLogin(mUsernameInput.getText().toString(),mPasswordInput.getText().toString());
            }
        });
    }

    /**
     * @brief Sends a post request to the login API endpoint with the username and password
     * and handles the response
     * @param username entered username
     * @param password entered password
     */
    public void handleLogin(String username,String password){
        Log.d("TEST",username.isEmpty()+" "+password.isEmpty());
        if(username.isEmpty() || password.isEmpty()){
            new AlertDialog.Builder(this)
                    .setTitle("Error")
                    .setMessage("Username or password is empty")
                    .show();
            return;
        }
        String params = String.format("{'username':'%s','password':'%s'}",username,password);
        CallAPI request = new CallAPI(new AsyncResponse() {
            @Override
            public void processFinish(String output) {
                Log.d("TEST","output:"+output);
                try {
                    JSONObject obj = new JSONObject(output);
                    String title=null;
                    String message = null;
                    if(obj.getString("status").equals("0")){
                        title="Wrong credentials";
                        message="Wrong username or password entered";
                        new AlertDialog.Builder(LoginActivity.this)
                                .setTitle(title)
                                .setMessage(message)
                                .show();
                    }
                    else if (obj.getString("status").equals("1")){
                        title="Login success";
                        message = "Correct credentials";
                        Intent myIntent = new Intent(LoginActivity.this, MainActivity.class);
                        startActivity(myIntent);
                    }


                }
                catch(Exception e){
                    e.printStackTrace();
                }
            }
        });
        request.execute(Urls.SERVER_URL+LOGIN_ENDPOINT,params);

    }

}
