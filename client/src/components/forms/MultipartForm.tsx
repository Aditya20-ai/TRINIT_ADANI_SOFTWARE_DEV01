import React, { useCallback, useEffect } from "react";


interface Props {
    children: React.ReactNode[];
    currentStep: number;
    formData: any;
    validateBeforeSubmit?: (data: any) => boolean;
    onSubmit: (data: any) => void;
}


const Form: React.FC<Props> = ({ children, currentStep, formData, validateBeforeSubmit, onSubmit }) => {
    const handleFormSubmit = () => {
        validateBeforeSubmit && validateBeforeSubmit(formData)
        onSubmit(formData);
    }

    if (currentStep > children.length) {
        handleFormSubmit();
    }
    
    return (<>
        {children}
    </>)
}

export default Form;