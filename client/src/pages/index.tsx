import React, { useEffect, useState } from "react";
import { type NextPage } from "next";
import Head from "next/head";
import Link from "next/link";
import { signIn, signOut, useSession } from "next-auth/react";

import TopBar from "../components/topbar";
import CompleteProfile from "../components/Complete";

import { api } from "../utils/api";
import { getUserData } from "../utils/funcs";

const Home: NextPage = () => {
  const hello = api.example.hello.useQuery({ text: "from tRPC" });

  const { data: sessionData } = useSession();
  const [user, setUser] = useState<any>(null);
  const [setupComplete, setSetupComplete] = useState<boolean | null>(null);

  useEffect(() => {
    if (sessionData?.user) {
      getUserData(sessionData.user.id).then((userData) => {
        console.log(userData);
        if (!userData) {
          setSetupComplete(false);
        } else {
          setSetupComplete(true);
          setUser(userData);
        }
      });
    }
  }, [sessionData]);


  return (
    <>
      <Head>
        <title>Gonate</title>
        <meta name="description" content="Linking resources to where they make a difference" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <TopBar />  
      {
        setupComplete
      }
      {
        setupComplete === false && <CompleteProfile />
      }
    </>
  );
};

export default Home;

const AuthShowcase: React.FC = () => {
  const { data: sessionData } = useSession();

  const { data: secretMessage } = api.example.getSecretMessage.useQuery(
    undefined, // no input
    { enabled: sessionData?.user !== undefined },
  );

  return (
    <div className="flex flex-col items-center justify-center gap-4">
      <p className="text-center text-2xl text-white">
        {sessionData && <span>Logged in as {sessionData.user?.name}</span>}
        {secretMessage && <span> - {secretMessage}</span>}
      </p>
      <button
        className="rounded-full bg-white/10 px-10 py-3 font-semibold text-white no-underline transition hover:bg-white/20"
        onClick={sessionData ? () => void signOut() : () => void signIn()}
      >
        {sessionData ? "Sign out" : "Sign in"}
      </button>
    </div>
  );
};
