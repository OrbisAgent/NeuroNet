export interface DataPoint {
  features: number[]
  label: number | string
  timestamp?: number
}

export interface Model {
  predict(data: DataPoint | DataPoint[]): number | number[]
  train(data: DataPoint[]): void
  setHyperparameter(param: string, value: number): void
  clone(): Model
  fineTune(data: DataPoint[]): void
  weights: { [key: string]: number[] }
}

export interface Hyperparameters {
  [key: string]: number
}

export interface User {
  id: string
}

export interface Contribution {
  quality: number
  impact: number
}

export interface ClientUpdate {
  weights: { [key: string]: number[] }
  timestamp: number
}

