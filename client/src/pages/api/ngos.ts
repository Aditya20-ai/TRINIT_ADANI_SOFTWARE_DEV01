import { NextApiRequest, NextApiResponse } from "next"


export const dummy = [
    {
        id: "1",
        name: "NGO 1",
        mission: "NGO 1 mission",
    },
    {
        id: "2",
        name: "NGO 2",
        mission: "NGO 2 mission",
    },
    {
        id: "3",
        name: "NGO 3",
        mission: "NGO 3 mission",
    },
]


export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    res.status(200).json(dummy)
}