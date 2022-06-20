import {Loading} from 'element-ui'

const loading = function(text) {
    return Loading.service({
        lock: true,
        text: text,
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
    });
};

export default loading;
