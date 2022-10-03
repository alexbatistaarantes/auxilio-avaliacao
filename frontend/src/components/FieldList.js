const FieldList = ({ fields }) => {
    
    return (
        <div className="field-list">
            <ul>
            {fields.map((field) => (
                <li key={ field.id } >
                    <div className="field-preview">
                        <h3>{ field.label }</h3>
                        <img src={ field.image } alt="" />
                    </div>
                </li>
            ))}
            </ul>
        </div>
    );
}

export default FieldList;
