import ReactCrop from 'react-image-crop';
import 'react-image-crop/dist/ReactCrop.css';

const SelectionTool = ({src, crop, onCropChange}) => {

    return (
        <div className="selection-tool">
            <div>
                <ReactCrop crop={crop} onChange={(_, c) => onCropChange(c)} scale={1}>
                    <img src={src} alt="" />
                </ReactCrop>
            </div>
        </div>
    );
}

export default SelectionTool;
