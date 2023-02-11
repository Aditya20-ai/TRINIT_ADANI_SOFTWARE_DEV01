import React from "react";

interface Props {
    label: string;
    options: string[];
    selectedOption: string;
    setSelectedOption: React.Dispatch<React.SetStateAction<string>>;
}

const SingleSelect: React.FC<Props> = ({ label, options, selectedOption, setSelectedOption }) => {
    return (<>
        <div className="flex flex-col w-full h-fit rounded-lg mt-3">
            <label className="text-xs font-medium text-neutral-700 mb-1" htmlFor={label}>{label}</label>
            <select className="border-b border-neutral-700" onChange={(e) => setSelectedOption(e.currentTarget.value)} name={label} >
                {
                    options.map((option, index) => {
                        return (
                            <option className={`${selectedOption === option ? "bg-neutral-200" : ""}`} key={index} value={option}>{option}</option>
                        )
                    })
                }
            </select>
        </div>
    </>)
}

export default SingleSelect;