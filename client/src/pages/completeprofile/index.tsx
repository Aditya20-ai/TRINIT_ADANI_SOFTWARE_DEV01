
import React, { useEffect } from "react"
import { useSession } from "next-auth/react"
import { signIn } from "next-auth/react"

import MultiSelect from "../../components/Multiselect"

import { createUserAccount, createNGOAccount } from "../../utils/funcs"

const APIENDPOINT = 'http://localhost:3000/api'

export interface UserData {
    name: string
    email: string
    preferences: string[]
}

export interface NgoData {
    name: string
    email: string
    mission: string
    history: string
    impact: string
    plans: string
    funding_needs: string
    location: string
    type: string
}

const NGO_TYPES = [
    "Environmental",
    "Social Welfare",
    "Animal Welfare",
    "Disaster Relief",
    "Education",
    "Health",
    "Microfinance",
    "Human Rights",
    "Women's Empowerment",
    "Children's Rights",
    "Disability Rights",
    "LGBTQ+ Rights",
    "Refugee and Migration",
    "Poverty Alleviation",
    "Agriculture and Rural Development",
    "Water and Sanitation",
    "Community Development",
    "Religious and Faith-Based",
    "Cultural Preservation",
    "Arts and Culture"
]

export default function CompleteProfile() {

    const { data: sessionData, status } = useSession()
    
    useEffect(() => {
        if (status === "unauthenticated") {
            signIn()
        }
    }, [status])

    const [accountType, setAccountType] = React.useState(0)
    const [ngoData, setNgoData] = React.useState<NgoData>({
        name: "",
        email: "",
        mission: "",
        history: "",
        impact: "",
        plans: "",
        funding_needs: "",
        location: "",
        type: ""
    })
    const [userData, setUserData] = React.useState<UserData>({
        name: "",
        email: "",
        preferences: []
    })


    
    if (accountType === 0) /* Not set */ {
        return (
            <div className="flex flex-col items-center justify-center gap-4">
                <p className="text-center text-2xl text-white">
                    What type of account do you want to create?
                </p>
                <div className="flex flex-row items-center justify-center gap-4">
                    <button className="font-inter px-11 py-4 bg-slate-600 rounded-lg text-white font-bold" onClick={() => setAccountType(1)}>NGO</button>
                    <button className="font-inter px-11 py-4 bg-slate-600 rounded-lg text-white font-bold" onClick={() => setAccountType(2)}>Individual</button>
                </div>
            </div>
        )
    }

    function validateAndCreateNgo() {
        if ( ngoData.name !== '' && ngoData.email !== '' && ngoData.mission !== '' && ngoData.history !== '' && ngoData.impact !== '' && ngoData.plans !== '' && ngoData.funding_needs !== '' && ngoData.location !== '' && ngoData.type !== '' ) {
            if (!sessionData?.user?.id) signIn()
            else createNGOAccount(ngoData, sessionData?.user?.id)
        } else {
            alert('Please fill all the fields')
        }
    }

    if (accountType === 1) /* NGO */ {
        return (
            <div className="flex flex-col items-center justify-center gap-4">
                <p className="text-center text-2xl">
                    What type of NGO are you?
                </p>
                <p>{JSON.stringify(ngoData)}</p>
                <div className="flex flex-col items-center justify-center gap-4">
                    <div className="flex">
                        {   
                            NGO_TYPES.map((name) =>{
                                return (<>
                                    <button className={`px-8 py-4 mb-4 mr-4 ${ngoData.type === name ? "bg-gray-800" : "bg-gray-600"} text-white`} onClick={(e) => {setNgoData({ ...ngoData, type: name })}}>
                                        {name}
                                    </button>
                                </>)    
                            })
                        }
                    </div>
                    <input className="border border-black" placeholder="Name" type="text" value={ngoData.name} onChange={(e) => {setNgoData({...ngoData, name: e.target.value})}} />
                    <input className="border border-black" placeholder="Email" type="text" value={ngoData.email} onChange={(e) => {setNgoData({...ngoData, email: e.target.value})}} />
                    <textarea className="border border-black" placeholder="history" value={ngoData.history} onChange={(e) => {setNgoData({...ngoData, history: e.target.value})}} name="mission" id="history" cols={30} rows={10}></textarea>
                    <textarea className="border border-black" placeholder="mission" value={ngoData.mission} onChange={(e) => {setNgoData({...ngoData, mission: e.target.value})}} name="mission" id="history" cols={30} rows={10}></textarea>
                    <textarea className="border border-black" placeholder="impact" value={ngoData.impact} onChange={(e) => {setNgoData({...ngoData, impact: e.target.value})}} name="mission" id="history" cols={30} rows={10}></textarea>
                    <textarea className="border border-black" placeholder="plans" value={ngoData.plans} onChange={(e) => {setNgoData({...ngoData, plans: e.target.value})}} name="mission" id="history" cols={30} rows={10}></textarea>
                    <textarea className="border border-black" placeholder="history" value={ngoData.history} onChange={(e) => {setNgoData({...ngoData, history: e.target.value})}} name="mission" id="history" cols={30} rows={10}></textarea>
                    <input className="border border-black" placeholder="Funding Needs" type="text" value={ngoData.funding_needs} onChange={(e) => {setNgoData({...ngoData, funding_needs: e.target.value})}} />
                    <input className="border border-black" placeholder="Location" type="text" value={ngoData.location} onChange={(e) => {setNgoData({...ngoData, location: e.target.value})}} />
                
                    <button onClick={validateAndCreateNgo}>
                        Create Account
                    </button>

                </div>
                
            </div>
        )
    }

    const handleOptionClick = (option: string) => {
        if (userData.preferences.includes(option)) {
            setUserData({...userData, preferences: userData.preferences.filter((o) => o !== option)});
        } else {
            setUserData({...userData, preferences: [...userData.preferences, option]});
        }
      };

    function validateAndCreateUser() {
        if (!userData.name || !userData.email) {
            alert("Please fill in all fields")
            return
        }

        if (!sessionData?.user?.id) signIn()
        else createUserAccount(userData, sessionData?.user?.id)


    }

    if (accountType === 2) /* Individual */ {
        return (<>
            {JSON.stringify(userData)}
            <div className="flex flex-col items-center justify-center gap-4">
                <input type="text" name="name" placeholder="Name" value={userData.name} onChange={(e) => { setUserData( { ...userData, name: e.target.value } ) }} required />
                <input type="email" name="name" placeholder="email" value={userData.email} onChange={(e) => { setUserData( { ...userData, email: e.target.value } ) }} required />
                <div className="relative">
                <button
                    className="bg-white text-gray-700 py-2 px-4 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-inset focus:ring-gray-300"
                    type="button"
                >
                    {userData.preferences.length
                    ? userData.preferences.map((option) => option).join(", ")
                    : "Select options"}
                </button>
                <div
                    className="absolute z-10 mt-2 py-2 bg-white border border-gray-300 rounded-lg shadow-xl"
                    style={{ minWidth: "100%" }}
                >
                    <ul className="list-reset">
                    {NGO_TYPES.map((option) => (
                        <li
                        key={option}
                        className={`px-4 py-2 hover:bg-gray-100 cursor-pointer ${
                            userData.preferences.includes(option)
                            ? "bg-gray-200 text-gray-800 font-medium"
                            : "text-gray-700"
                        }`}
                        onClick={() => handleOptionClick(option)}
                        >
                        {option}
                        </li>
                    ))}
                    </ul>
                    <button onClick={validateAndCreateUser}>Create</button>
                </div>
                </div>
            </div>
        </>)
    }
    
}

