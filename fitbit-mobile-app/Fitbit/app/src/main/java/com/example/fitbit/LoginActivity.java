package com.example.fitbit;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.app.AlertDialog;
public class LoginActivity extends Activity {
    public static final String LOGIN_ENDPOINT="/login";
    private Button mLoginBtn;
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
        CallAPI request = new CallAPI();
        request.execute(Urls.SERVER_URL+LOGIN_ENDPOINT);

    }

}
