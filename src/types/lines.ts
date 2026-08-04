export type LineName =
  | 'S1'
  | 'S15'
  | 'S2'
  | 'S25'
  | 'S26'
  | 'S3'
  | 'S41'
  | 'S42'
  | 'S46'
  | 'S47'
  | 'S5'
  | 'S7'
  | 'S8'
  | 'S85'
  | 'S9'
  | 'U1'
  | 'U2'
  | 'U3'
  | 'U4'
  | 'U5'
  | 'U6'
  | 'U7'
  | 'U8'
  | 'U9'

export type Line = {
  name: LineName
  color: string
  textColor: string
}

export type LineStop = {
  name: string
  lines: Array<LineName>
  zone: 'A' | 'B' | 'C'
}
