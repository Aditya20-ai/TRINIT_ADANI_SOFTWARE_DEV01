import React, { useEffect } from "react";

import { useRouter } from "next/router";

interface NGO {
    id: string;
    name: string;
    mission: string;
    history: string;
    immpact: string
    plans: string;
    funding_needs: string;
    location: string;
    type: string;
}

function getNGO(id: string) {
    return {
        id: "1",
        name: "testname",
        mission: "testmission",
        history: "testhistory",
        immpact: "testimpact",
        plans: "testplans",
        funding_needs: "testfundingneeds",
        location: "testlocation",
        type: "testtype"
    }
}

export default function index() {
    const router = useRouter();
    const { ngoid } = router.query;

    const [data, setData] = React.useState<NGO | null>(null);

    
    useEffect(() => {
        const ngo = getNGO(ngoid as string);
        setData(ngo);
    }, [])
    
    if (!data) {
        return <div>loading...</div>
    }

    return (
        <div className="flex flex-col m-20 p-6 shadow-lg bg-neutral-100">
            <h1 className="text-center font-bold text-2xl">{data.name}</h1>
            <h2 className="font-bold text-lg mt-6">Mission</h2>
            <p>{data.mission}</p>
            <h2 className="font-bold text-lg mt-6">History</h2>
            <p>{data.history}</p>
            <h2 className="font-bold text-lg mt-6">Impact</h2>
            <p>{data.immpact}</p>
            <h2 className="font-bold text-lg mt-6">Plans</h2>
            <p>{data.plans}</p>
            <h2 className="font-bold text-lg mt-6">Funding Needs</h2>
            <p>{data.funding_needs}</p>
            <h2 className="font-bold text-lg mt-6">Location</h2>
            <p>{data.location}</p>
            <h2 className="font-bold text-lg mt-6"> Type</h2>
            <p>{data.type}</p>
        </div>
    )
}