const FieldList = ({ fields }) => {
    
    return (
        <div className="field-list">
            <ul>
            {fields.map((field) => (
                <li key={ field.id } >
                    <div className="field-preview">
                        <h4>{ field.label }</h4>
                        <img className="document-crop" src={ field.image } alt="" />
                    </div>
                </li>
            ))}
            </ul>
        </div>
    );
}

export default FieldList;
