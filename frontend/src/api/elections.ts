/* eslint-disable @typescript-eslint/camelcase */

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

export interface ApiElectionInterface {
  id: number;
  title: string;
  description: string;
  questions: ApiQuestion[];
  created_at: string;
  public_key: string;
  state: "CREATED" | "OPENED" | "CLOSED";
  is_owned: boolean;
  permissions: Array<string>;
}

export class ApiElection implements ApiElectionInterface {
  created_at: string;
  description: string;
  id: number;
  is_owned: boolean;
  permissions: Array<string>;
  public_key: string;
  questions: ApiQuestion[];
  state: "CREATED" | "OPENED" | "CLOSED";
  title: string;

  constructor(
    created_at: string,
    description: string,
    id: number,
    is_owned: boolean,
    permissions: Array<string>,
    public_key: string,
    questions: ApiQuestion[],
    state: "CREATED" | "OPENED" | "CLOSED",
    title: string
  ) {
    this.created_at = created_at;
    this.description = description;
    this.id = id;
    this.is_owned = is_owned;
    this.permissions = permissions;
    this.public_key = public_key;
    this.questions = questions;
    this.state = state;
    this.title = title;
  }
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
