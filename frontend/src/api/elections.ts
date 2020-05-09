export interface ApiAnswer {
  id: number,
  text: string,
  question: number,
}

export interface ApiQuestion {
  id: number,
  question: string,
  answers: ApiAnswer[],
  election: number,
}

export interface ApiElection {
  id: number,
  title: string,
  description: string,
  questions: ApiQuestion[],
  state: "CREATED" | "OPENED" | "FROZEN",
  is_owned: boolean
}
