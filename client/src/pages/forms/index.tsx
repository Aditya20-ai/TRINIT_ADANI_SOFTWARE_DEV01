import { 
    TextField,
    NumericField,
    TextAreaField,
    SingleCheck,
    MultiCheck,
    GroupCheck,
    SingleSelect,
    MultiSelect
} from "../../components/forms";


import FormStep from "../../components/forms/FormStep";
import Form from "../../components/forms/MultipartForm";

import { useState } from "react";


export default function CompleteProfile() {
    const [name, setName] = useState("");
    const [age, setAge] = useState(0);
    const [bio, setBio] = useState("");
    const [isDisabled, setIsDisabled] = useState(false);
    const [interests, setInterests] = useState<string[]>([]);
    const [gender, setGender] = useState("");
    const [selectedOption, setSelectedOption] = useState("");
    const [selectedOptions, setSelectedOptions] = useState<string[]>([]);

    const formState = {
        name,
        age,
        bio,
        isDisabled,
        interests,
        gender,
        selectedOption,
        selectedOptions
    }

    const [currentStep, setCurrentStep] = useState(1);
    
    return (
        <div className="w-2/5 border border-neutral-700 p-6">
            {JSON.stringify(formState)}
            
            <Form formData={formState} currentStep={currentStep} onSubmit={(data) => console.log("Form submitted: ", data)}>
                <FormStep currentStep={currentStep} stepIndex={1}>
                    <TextField label="Name" value={name} setValue={setName} />
                    <NumericField label="Age" value={age} setValue={setAge} />
                    <button onClick={(e) => setCurrentStep(currentStep+1)}>Next</button>
                </FormStep>
                <FormStep currentStep={currentStep} stepIndex={2}>
                    <TextAreaField label="Bio" value={bio} setValue={setBio} />
                    <SingleCheck label="Are you disabled?" value={isDisabled} setValue={setIsDisabled} />
                    <button onClick={(e) => setCurrentStep(currentStep+1)}>Next</button>
                </FormStep>
                <FormStep currentStep={currentStep} stepIndex={3}>
                    <MultiCheck label="Interests" options={["Music", "Sports", "Movies"]} selectedOptions={interests} setSelectedOptions={setInterests} />
                    <MultiSelect label="Interests" options={["Music", "Sports", "Movies"]} selectedOptions={interests} setSelectedOptions={setInterests} />
                    <button onClick={(e) => setCurrentStep(currentStep+1)}>Submit</button>
                </FormStep>
            </Form>    

        </div>
    )
}