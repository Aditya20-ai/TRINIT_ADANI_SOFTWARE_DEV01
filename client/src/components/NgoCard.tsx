import React from "react";


export interface NgoCardProps {
    name: string;
    mission: string;
    id: string;
}


export default function NgoCard(ngo: NgoCardProps) {
    const { name, mission, id } = ngo;
    return (
        <a data-ngo={JSON.stringify(ngo)} href={`/ngos/${id}`}>
            <div className="w-[400px] p-4 bg-neutral-300 mb-2 mr-2 rounded-lg">
                <h1 className="font-bold text-xl">{name}</h1>
                <p className=" text-neutral-600">{mission}</p>
                <a className="font-inter text-right block text-sm text-neutral-500" href={`/ngos/${id}`}>View -&gt;</a>
            </div>
        </a>
    );
}