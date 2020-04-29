package com.example.fitbit;

import android.content.Intent;
import android.os.Bundle;
import android.text.Html;
import android.text.TextUtils;
import android.text.method.LinkMovementMethod;
import android.util.Patterns;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Toast;


import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;


public class SignUpActivity extends AppCompatActivity {
    private static final String TAG = "SignupActivity";
    EditText username;
    EditText password;
    EditText email;
    EditText rePassword;
    CheckBox termOfUse;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_up);
        username=findViewById(R.id.editTextUsernameSignUp);
        password=findViewById(R.id.editTextPasswordSignUp);
        email=findViewById(R.id.editTextEmail);
        rePassword=findViewById(R.id.editTextRePasswordSignUp);
        termOfUse=findViewById(R.id.termOfUseCheckBox);
        String TermsOfUse="I acknowledge that i agree to the <br><a href=\""+Urls.FRONT_END_URL+"/TermsAndConditions\">Terms of Use</a>,<a href=\""+Urls.FRONT_END_URL+"/PrivacyPolicy\"> Privacy Policy</a> and <a href=\""+Urls.FRONT_END_URL+"/CookiesPolicy\">Cookies Policy</a>";
        termOfUse.setText(Html.fromHtml(TermsOfUse));
        termOfUse.setMovementMethod(LinkMovementMethod.getInstance());
        findViewById(R.id.buttonSignUp).setOnClickListener((view)->{
            if(username.getText().toString().trim().equals("")){
                username.setError("You must provide a username");
                return;
            }else if(TextUtils.isEmpty(email.getText()) || !Patterns.EMAIL_ADDRESS.matcher(email.getText()).matches()){
                email.setError("You must provide a valid email");
                return;
            }else if(password.getText().toString().equals("")){
                password.setError("You must provide a password");
                return;
            }else if(!password.getText().toString().equals(rePassword.getText().toString())){
                rePassword.setError("Password are not matching");
                return;
            }else if(!termOfUse.isChecked()){
                termOfUse.setError("You must read and accept our policy");
                return;
            }
            CallAPI request=new CallAPI("POST", output -> {
                try {
                    JSONObject obj = new JSONObject(output);
                    if(obj.has("error")){
                        if(obj.getString("error").equals("username already exists")){
                            username.setError("Username already exists");
                        }
                        else {
                            Toast.makeText(SignUpActivity.this,obj.getString("error"),Toast.LENGTH_SHORT).show();
                        }
                    }else if(obj.has("status")){
                        Intent myIntent = new Intent(SignUpActivity.this, MainActivity.class);
                        startActivity(myIntent);
                    }

                } catch (JSONException e) {
                    e.printStackTrace();
                }

            });
            request.execute(Urls.SERVER_URL+Urls.SIGNUP_ENDPOINT,"username",username.getText().toString(),"password",password.getText().toString(),"repeat_password",rePassword.getText().toString(),"email",email.getText().toString());
        });

        findViewById(R.id.textViewLogin).setOnClickListener((view)->{
            Intent myIntent= new Intent(SignUpActivity.this,LoginActivity.class);
            startActivity(myIntent);
        });

    }


}
