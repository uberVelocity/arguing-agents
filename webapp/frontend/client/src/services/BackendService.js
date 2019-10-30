import axios from 'axios';

class BackendService {

    static async processTopic(topic) {
        return await axios.post('http://localhost:5000/process', {
            topic
        });
    }
}

export default BackendService;