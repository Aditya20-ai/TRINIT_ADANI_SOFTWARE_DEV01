import React from "react";
import NgoCard, { NgoCardProps } from "../../components/NgoCard";

import TopBar from "../../components/topbar";


export default function Ngos() {

    const [ngos, setNgos] = React.useState<NgoCardProps[]>([])
    React.useEffect(() => {
        fetch("http://localhost:3000/api/campaigns")
            .then(res => res.json())
            .then(data => setNgos(data))
    }, [])

    return (<>
        <TopBar />
        <div className="lg:px-20 px-4 lg:pt-16 pt-6">
            <h1 className="text-4xl font-bold">Ngos</h1>
            <div>
                filters
            </div>
            <div className="flex w-full">
                {
                    ngos ? ngos.map(ngo => (
                        <NgoCard
                            key={ngo.id}
                            name={ngo.name}
                            mission={ngo.mission}
                            id={ngo.id}
                        />
                    )) : 
                    <p>Loading...</p>
                }
            </div>
        </div>
    </>);
}
