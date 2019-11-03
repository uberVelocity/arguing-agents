import axios from 'axios';

class BackendService {

    static async processTopic(topic, similarity_measure) {
        return await axios.post('http://localhost:5000/process', {
            topic_name: topic,
            similarity_measure: similarity_measure
        });
    }
}

export default BackendService;