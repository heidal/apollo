import { Server, Model } from "miragejs";

export function makeServer({ environment = "development" } = {}) {

  const djangoListResponse = results => {
    return {
      count: results.length,
      results: results.models
    };
  };

  const server = new Server({
    environment,

    models: {
      election: Model
    },

    seeds(server) {
      server.create("election", {
        id: 1,
        title: "First election!",
        description: "A great election to vote in",
        questions: [
          {
            id: 1,
            question: "First question!"
          },
          {
            id: 2,
            question: "Second question"
          }
        ]
      });
      server.create("election", {
        id: 2,
        title: "Second election!",
        description: "Also great election",
        questions: [
          {
            id: 3,
            question: "First question!"
          },
          {
            id: 4,
            question: "Second question"
          }
        ]
      });
      server.create("election", {
        id: 3,
        title: "Is this a third election?",
        description: "Sure it is!",
        questions: [
          {
            id: 5,
            question: "First question!"
          },
          {
            id: 6,
            question: "Second question"
          }
        ]
      });
    },

    routes() {
      this.namespace = "api";

      // TODO left here for documentation purposes
      // this.get("/elections/elections/", schema => {
      //   return djangoListResponse(schema.elections.all());
      // });

      this.passthrough();
    }
  });

  return server;
}
