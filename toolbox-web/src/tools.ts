import {Tool} from "@/models";

export const tools: Tool[] = [
  {name: "FlameGraph", icon: "mdi-bug"},
  {name: "Spectrograph", icon: "mdi-music"},
  {name: "pev2", icon: "mdi-bug"},
]

export const toolByName = (name: string) => {
  return tools.find(t => t.name == name)
}
