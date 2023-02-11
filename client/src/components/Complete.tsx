import React from "react";


import { useRouter } from "next/router";


export default function CompleteProfile() {

    const router = useRouter();

    return (<>

        <div>
            <button onClick={(e) => router.push('/completeprofile')} className="font-inter px-11 py-4 bg-slate-600 rounded-lg text-white font-bold">Complete profile setup -&gt;</button>
        </div>
    
    </>)

}