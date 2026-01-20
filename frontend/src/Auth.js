// src/auth.js
export function saveUser(user) {
    localStorage.setItem("user", JSON.stringify(user));
  }
  
  export function getUser() {
    return JSON.parse(localStorage.getItem("user"));
  }
  
  export function logout() {
    localStorage.removeItem("user");
  }
  