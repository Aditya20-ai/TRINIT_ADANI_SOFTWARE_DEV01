async function getUserData(userId: string) {

    return null /* dev */

    const response = await fetch("URL", { method: "POST", body: JSON.stringify({ userId }), headers: { "Content-Type": "application/json" } });
    const data = await response.json();
    return data;
} 

import { UserData, NgoData } from "../pages/completeprofile";

async function createUserAccount(data: UserData, userId: string) {
    
    console.log("create user with data: ",data, userId)
    return true /* dev */
    
    const response = await fetch("URL", { method: "POST", body: JSON.stringify({...data, userId}), headers: { "Content-Type": "application/json" } });
    const d = await response.json();
    return d;
}

async function createNGOAccount(data: NgoData, userId: string) {
    
    console.log("create ngo with data: ", data, userId)
    return true /* dev */

    const response = await fetch("URL", { method: "POST", body: JSON.stringify({...data, userId}), headers: { "Content-Type": "application/json" } });
    const d = await response.json();
    return d;
}

export {
    getUserData, 
    createUserAccount, 
    createNGOAccount
}