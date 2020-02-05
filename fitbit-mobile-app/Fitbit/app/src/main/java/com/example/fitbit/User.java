package com.example.fitbit;
/*
Class that represents User. Holds JWT and username.
Follows singleton pattern
 */
public class User {
    private static User user;
    private static String username,jwt;
    private User(){}
    public static User getUser(){
        if(user==null) {
            user = new User();
        }
        return user;
    }
    public static void setUsername(String username){
        User.username = username;
    }
    public static void setJWT(String jwt){
        User.jwt=jwt;
    }
    public static String getJWT(){
        return jwt;
    }
    public static String getUsername(){
        return username;
    }


}
