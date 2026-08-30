import axios from 'axios'

export async function analyze(resume: string, job: string) {
  const resp = await axios.post('/api/analyze', { resume, job })
  return resp.data
}
