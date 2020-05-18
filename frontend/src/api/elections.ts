export interface ApiAnswer {
  id: number;
  text: string;
  question: number;
}

export interface ApiQuestion {
  id: number;
  question: string;
  answers: ApiAnswer[];
  election: number;
}

export interface APIElection {
  id: number;
  title: string;
  description: string;
  questions: ApiQuestion[];
  created_at: string;
  public_key: string;
  state: "CREATED" | "OPENED" | "CLOSED";
  is_owned: boolean;
}

export interface ApiElectionSummary {
  id: number;
  title: string;
  description: string;
  questions: {
    id: number;
    question: string;
    answers: {
      id: number;
      votes: number;
      text: string;
    }[];
  }[];
}
